from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shopify/", views.shopify, name="shopify"),
    path("wordpress/", views.wordpress, name="wordpress"),
    path("ecommerce/", views.ecommerce, name="ecommerce"),
    path("webdesign/", views.webdesign, name="webdesign"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("marketing/", views.marketing, name="marketing"),
    path("seo/", views.seo, name="seo"),
    path("graphic-design/", views.graphic_design, name="graphic_design"),
    path("other-services/", views.other_services, name="other_services"),
    path("software-services/", views.software_services, name="software_services"),
    
    path("contact/", views.contact, name="contact"),
]