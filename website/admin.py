
from django.contrib import admin
from .models import Banner, OzbixFolio
from .models import Service
from .models import Client


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['image']

@admin.register(Service)
class serviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

@admin.register(OzbixFolio)
class OzbixfolioAdmin(admin.ModelAdmin):
    list_display = ["id",'image']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','image']