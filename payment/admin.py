from django.contrib import admin
from .models import Product, userCart, cartItems, Reviews, Orders

admin.site.register(Product)
admin.site.register(userCart)
admin.site.register(cartItems)
admin.site.register(Reviews)
admin.site.register(Orders)