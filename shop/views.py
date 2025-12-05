from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LogInForm, reviewForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from payment.models import Product, userCart, cartItems, Reviews, Orders
import google.generativeai as genai
import random
import threading


def aiSummary(reviews):
    genai.configure(api_key="AIzaSyC1ws0DtcH9r0dH_k05ih4NwsPeEMcL1Lo") 

    
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"(type nothing else)summarize these product reviews from different people and provide a short, simple and professional summary on what they think about it:\n\n\n{reviews}"

    response = model.generate_content(prompt)
    
    return (response.text)

def unify(obj):
    lis = []
    for i in obj:
        if i.category not in lis:
            lis.append(i.category)
    return lis
    


@login_required(login_url='/signup/')
def listing(request):
    products = Product.objects.all()
    copy = products
    query = request.GET.get('q')
    toVal, fromVal = request.GET.get('to'), request.GET.get('from')
    catVal = request.GET.get('category')
    ratingVal = request.GET.get('rating')

    if toVal or fromVal:
        try:
            toVal = float(toVal)
        except ValueError:
            toVal = 0.0
        try:
            fromVal = float(fromVal)
        except ValueError:
            fromVal = 0.0
        if toVal == 0.0:
            products = products.filter(price__gte = fromVal)
        else:
            products = products.filter(price__gte = fromVal, price__lte = toVal)
    
    if catVal:
        products = products.filter(category=catVal)

    if ratingVal:
        products = products.filter(starRating__gte = 3)

    if query:
        products = products.filter(name__icontains=query)
    return render(request, "listing.html", {"products": products, "category":unify(copy)})


@login_required(login_url='/signup/')
def ordersView(request):
    ord = Orders.objects.filter(user = request.user)
    return render(request, "ordersView.html", {"ord":ord})


def send_otp_email(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def addToCart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        productQuantity = request.POST.get("quantity")
        prod = Product.objects.get(id=product_id)
        user_cart, created = userCart.objects.get_or_create(user=request.user)
        cart_item, created = cartItems.objects.get_or_create(cart=user_cart, product_id=product_id)

        cart_item.amount += int(prod.price * int(productQuantity))
        
        cart_item.quantity += int(productQuantity)

        cart_item.save()
        return redirect(request.META.get('HTTP_REFERER', 'listing'))


def removeFromCart(request, item_id):
    if request.method == "POST":
        user_cart = userCart.objects.filter(user=request.user).first()
        if user_cart:
            cart_item = cartItems.objects.filter(cart=user_cart, id=item_id).first()
            if cart_item:
                cart_item.delete()
        return redirect("CartView")

def LogOut(request):
    logout(request)
    return redirect("signup")

def signupView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            token = str(random.randint(100000, 999999))
            request.session['otp'] = token
            request.session['signUpData'] = form.cleaned_data

            send_otp_email(
                'Verify your email',
                f'Your verification code is {token}',
                'akshajphotodrive@gmail.com',
                [form.cleaned_data['email']]
            )
            return redirect("verify_otp")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/signup/')
def verify_otp(request):
    error = None
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        real_otp = request.session.get("otp")
        if entered_otp == real_otp:
            signUpData = request.session.get("signUpData")
            form = CustomUserCreationForm(signUpData)
            if form.is_valid():
                form.save()
                request.session.pop('otp', None)  # Clear OTP from session
                request.session.pop('signUpData', None)  # Clear signUpData from session
                return redirect("listing")

            else:
                error = "Form is invalid."

        else:
            error = "Invalid OTP. Please try again."
    return render(request, "verify_otp.html", {"error": error})


def loginView(request):
    error = None
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("listing")
            else:
                error = "Invalid credentials"
        else:
            error = "Please correct the errors below."
    else:
        form = LogInForm()
    return render(request, "LogIn.html", {"form": form, "error": error})

@login_required(login_url='/signup/')
def productDetail(request, item_id):
    product = Product.objects.filter(id=item_id).first()
    if not product:
        return render(request, "404.html", status=404)
    product_reviews = Reviews.objects.filter(product=product).order_by('-id')
    return render(request, "productDetail.html", {"product": product, "reviews": product_reviews})

@login_required(login_url='/signup/')
def CartView(request):
    user_cart = userCart.objects.filter(user=request.user).first()
    if not user_cart:
        return render(request, "cartView.html", {"items": []})

    cart_items = cartItems.objects.filter(cart=user_cart)
    subTotal = 0

    for item in cart_items:
        subTotal += item.product.price * item.quantity
    

    return render(request, "cartView.html", {"items": cart_items, "subTotal": subTotal})


class SummaryThread(threading.Thread):
    def __init__(self, product, revList):
        super().__init__()
        self.product = product
        self.revList = revList
    def run(self):
        self.product.summary = aiSummary(self.revList)

@login_required(login_url='/signup/')
def reviewProduct(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if product == None:
        return render(request, "404.html", status=404)
    error = None
    # Prevent multiple reviews by same user for this product
    existing_review = Reviews.objects.filter(product=product, user=request.user).first()
    if existing_review:
        error = {"__all__": ["You have already reviewed this product."]}
        return render(request, "writeReview.html", {'form': reviewForm(), 'error': error, 'product': product})
    if request.method == "POST":
        form = reviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            comment = form.cleaned_data["comment"]
            Reviews.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )

            product_reviews = Reviews.objects.filter(product=product).order_by('-id')

            avgRat = 0
            count = 0
            for i in product_reviews:
                count+=1
                avgRat+=int(i.rating)
            avgRat = round(avgRat/count, 1)
            product.starRating = avgRat

            revList = ""
            for i in product_reviews:
                revList+=(str(i.comment)+"\n")
            SummaryThread(product, revList).start()
            product.save()
            return redirect("productDetail", item_id=product.id)
        else:
            error = form.errors
    else:
        form = reviewForm()
    return render(request, "writeReview.html", {'form': form, 'error': error, 'product': product})