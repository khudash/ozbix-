from multiprocessing.connection import Client

from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def shopify(request):
    return render(request, "shopify.html")

def wordpress(request):
    return render(request, "wordpress.html")

def ecommerce(request):
    return render(request, "e-commerce.html")

def webdesign(request):
    return render(request, "web-design.html")

def portfolio(request):
    return render(request, "portfolio.html")



from django.shortcuts import render
from .models import Banner, OzbixFolio
from .models import Service
from .models import Client

def home(request):
    banner = Banner.objects.first()
    services = Service.objects.all()
    ozbix_folios = OzbixFolio.objects.all()
    clients = Client.objects.all()

    context = {
        "banner": banner,
        "services": services,
        "ozbix_folios": ozbix_folios,
        "clients": clients
    }
    return render(request, "index.html", context)
