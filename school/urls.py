from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("over-ons/", views.about, name="about"),
    path("pakketten/", views.packages, name="packages"),
    path("contact/", views.contact, name="contact"),
]
