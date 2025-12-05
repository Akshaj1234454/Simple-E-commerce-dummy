"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.listing, name="listing"),
    path("signup/", views.signupView, name="signup"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("LogOut/", views.LogOut, name="LogOut"),
    path("login/", views.loginView, name="LogIn"),
    path("product/<int:item_id>/", views.productDetail, name="productDetail"),
    path("addToCart/", views.addToCart, name="addToCart"),
    path("cart/", views.CartView, name="CartView"),
    path("removeFromCart/<int:item_id>/", views.removeFromCart, name="removeFromCart"),
    path("review/<int:product_id>", views.reviewProduct, name = "writeReview"),
    path("orders/", views.ordersView, name = "ordersView"),
    path("payment/", include("payment.urls")),
    
    
]
