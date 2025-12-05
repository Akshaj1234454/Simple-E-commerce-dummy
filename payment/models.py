from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    summary = models.TextField(default="Error loading the summary.")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(default=None)
    starRating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
class userCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class cartItems(models.Model):
    cart = models.ForeignKey(userCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}"
    
class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} on {self.product.name}"

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkOutCart = models.ManyToManyField(cartItems)
    payAmount = models.IntegerField(default=0)
    address = models.TextField(max_length=100)
    pinCode = models.IntegerField(default = 0)
    mobileNumber = models.IntegerField(default = 0)
    orderDate = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"Order of: {self.user}"
    

