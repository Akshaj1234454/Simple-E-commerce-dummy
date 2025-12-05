from django.urls import path, include
from . import views



urlpatterns = [
    path("", views.checkOut, name ="checkOut"),
    path("handlepayment/", views.handlepayment, name="handlepayment"),
]
