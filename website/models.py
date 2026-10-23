from django.db import models


# ============================================================
# Banner — Homepage hero banner image
# ============================================================
class Banner(models.Model):
    image = models.ImageField(upload_to="banner/")

    def __str__(self):
        return str(self.image)


# ============================================================
# Service — Dynamic services shown on homepage & service pages
# ============================================================
class Service(models.Model):
    icon_class         = models.CharField(max_length=100)
    title              = models.CharField(max_length=100)
    short_description  = models.CharField(max_length=150)
    description        = models.TextField()
    button_text        = models.CharField(max_length=50, default="Read More")

    def __str__(self):
        return self.title


# ============================================================
# OzbixFolio — Portfolio showcase items
# ============================================================
class OzbixFolio(models.Model):
    image = models.ImageField(upload_to="ozbixfolio/")
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# ============================================================
# Client — Client logos
# ============================================================
class Client(models.Model):
    image = models.ImageField(upload_to="clients/")

    def __str__(self):
        return "Client Image"


# ============================================================
# ContactSubmission — Website contact form submissions
# ============================================================
class ContactSubmission(models.Model):
    full_name  = models.CharField(max_length=150)
    email      = models.EmailField()
    phone      = models.CharField(max_length=50, blank=True, null=True)
    services   = models.CharField(max_length=255, blank=True, null=True)
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.email})"


# ============================================================
# PageHero — Dynamic hero section for every service page
# Page choices match URL names
# ============================================================
class PageHero(models.Model):
    PAGE_CHOICES = [
        ('home',             'Home Page'),
        ('shopify',          'Shopify Page'),
        ('wordpress',        'WordPress Page'),
        ('ecommerce',        'E-Commerce Page'),
        ('webdesign',        'Web Design Page'),
        ('marketing',        'Marketing Page'),
        ('seo',              'SEO Page'),
        ('graphic_design',   'Graphic Design Page'),
        ('software_services','Software Services Page'),
        ('other_services',   'Other Services Page'),
        ('portfolio',        'Portfolio Page'),
    ]

    page        = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    heading     = models.CharField(max_length=200, blank=True, default='')
    subheading  = models.CharField(max_length=300, blank=True, default='')
    description = models.TextField(blank=True, default='')
    button_text = models.CharField(max_length=100, blank=True, default='Get Started')
    button_link = models.CharField(max_length=200, blank=True, default='#')
    image       = models.ImageField(upload_to="page_heroes/", blank=True, null=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return f"Hero — {self.get_page_display()}"


# ============================================================
# PageFeature — Dynamic feature cards/bullet points per page
# ============================================================
class PageFeature(models.Model):
    page        = models.CharField(max_length=50)
    icon_class  = models.CharField(max_length=100, default='fas fa-check-circle')
    title       = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.page} — {self.title}"


# ============================================================
# Testimonial — Client reviews for homepage/portfolio pages
# ============================================================
class Testimonial(models.Model):
    client_name  = models.CharField(max_length=100)
    company      = models.CharField(max_length=100, blank=True, default='')
    country      = models.CharField(max_length=100, blank=True, default='')
    message      = models.TextField()
    avatar       = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    rating       = models.PositiveSmallIntegerField(default=5)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} — {self.company}"


# ============================================================
# SiteSettings — Global site-wide settings controllable from dashboard
# ============================================================
class SiteSettings(models.Model):
    site_name          = models.CharField(max_length=100, default='Ozbix IT Solutions')
    tagline            = models.CharField(max_length=255, default='Your Digital Growth Partner')
    email              = models.EmailField(default='info@ozbix.com')
    phone_pk           = models.CharField(max_length=30, default='+92 311 456 324')
    phone_uae          = models.CharField(max_length=30, default='+971 50 831 2016')
    phone_au           = models.CharField(max_length=30, default='+61 469 389 357')
    whatsapp_number    = models.CharField(max_length=30, default='+923175448546')
    facebook_url       = models.URLField(blank=True, default='#')
    instagram_url      = models.URLField(blank=True, default='#')
    twitter_url        = models.URLField(blank=True, default='#')
    linkedin_url       = models.URLField(blank=True, default='#')
    address            = models.TextField(blank=True, default='')
    footer_description = models.TextField(
        default='Ozbix Development House is Pakistan, Australian and Dubai based company that can work with professional team and always gives customer a great service.'
    )
    logo               = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon            = models.ImageField(upload_to='site/', blank=True, null=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj