# Built-in Django Admin Panel has been disabled.
# All dynamic models, services, clients, banners, portfolios,
# site settings, heroes, and testimonials are managed exclusively
# through the custom responsive dashboard at /dashboard/

from django.contrib import admin
from .models import (
    Banner, OzbixFolio, Service, Client,
    ContactSubmission, PageHero, PageFeature,
    Testimonial, SiteSettings
)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'button_text']
    search_fields = ['title']


@admin.register(OzbixFolio)
class OzbixFolioAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'is_read', 'created_at']
    list_filter  = ['is_read', 'created_at']
    search_fields = ['full_name', 'email', 'message']


@admin.register(PageHero)
class PageHeroAdmin(admin.ModelAdmin):
    list_display = ['page', 'heading', 'is_active']
    list_filter  = ['page', 'is_active']


@admin.register(PageFeature)
class PageFeatureAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'order']
    list_filter  = ['page']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company', 'country', 'rating', 'is_active']
    list_filter  = ['is_active', 'rating']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'email', 'phone_pk']