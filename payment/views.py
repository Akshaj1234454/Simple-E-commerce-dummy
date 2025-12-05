from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from .models import Orders, userCart, cartItems
from .forms import CheckoutForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paytm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

@login_required(login_url='/signup/')
def checkOut(request):
    user_cart = userCart.objects.filter(user=request.user).first()
    cart_items = cartItems.objects.filter(cart = user_cart)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payAmount = 0
            for i in cart_items:
                payAmount+=i.amount
            
            address = form.cleaned_data["address"]
            pinCode = form.cleaned_data["pinCode"]
            mobileNumber = form.cleaned_data["mobileNumber"]
            order = Orders.objects.create(
                user = request.user,
                address = address,
                pinCode = pinCode,
                mobileNumber = mobileNumber,
                payAmount = payAmount,
            )
            order.checkOutCart.set(cart_items)
            param_dict = {
                'MID': 'WorldP64425807474247',
                'ORDER_ID': str(order.pk),
                'TXN_AMOUNT': str(order.payAmount),
                'CUST_ID': request.user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/payment/handlepayment/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'paytm.html', {'param_dict':param_dict})
    else:
        form = CheckoutForm()
    return render(request, 'checkOut.html', {'form': form, 'items' : cart_items})

@login_required(login_url='/signup/')
@csrf_exempt
def handlepayment(request):
    return HttpResponse("done")