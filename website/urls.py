from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shopify/", views.shopify, name="shopify"),
    path("wordpress/", views.wordpress, name="wordpress"),
    path("ecommerce/", views.ecommerce, name="ecommerce"),
    path("webdesign/", views.webdesign, name="webdesign"),
    path("portfolio/", views.portfolio, name="portfolio"),
]