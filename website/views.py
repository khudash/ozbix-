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

def marketing(request):
    return render(request, "marketing.html")

def seo(request):
    return render(request, "seo.html")

def graphic_design(request):
    return render(request, "graphic-design.html")

def other_services(request):
    return render(request, "other-services.html")

def software_services(request):
    return render(request, "software-services.html")




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


# =====  Email ===== 

from django.shortcuts import render, redirect
from django.core.mail import send_mail

def contact(request):
    if request.method == "POST":


        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        services = request.POST.getlist("services")
        message = request.POST.get("message")
        services_text = ", ".join(services)
        email_message = f"""
New Let's Talk Form Submission

Name: {full_name}
Email: {email}
Phone: {phone}

Services:
{services_text}

Message:
{message}
"""

        send_mail(
            subject=f"New Website Inquiry - {full_name}",
            message=email_message,
            from_email="khudashkhan489@gmail.com",
           recipient_list=["khudashkhan489@gmail.com"],
        )

        return redirect("home")

    return redirect("home")