from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .models import (
    Banner, Service, OzbixFolio, Client,
    ContactSubmission, PageHero, PageFeature,
    Testimonial, SiteSettings
)
import os


# ─────────────────────────────────────────────────────────────
# HELPER — builds the common context used on every public page
# ─────────────────────────────────────────────────────────────
def _get_site_ctx():
    """Return site-wide context available on all public pages."""
    return {
        'site': SiteSettings.get_settings(),
        'all_services': Service.objects.all(),
    }


def _page_ctx(page_name):
    """Return hero + features for a given page slug."""
    hero     = PageHero.objects.filter(page=page_name, is_active=True).first()
    features = PageFeature.objects.filter(page=page_name)
    return {'hero': hero, 'features': features}


# ─────────────────────────────────────────────────────────────
# PUBLIC WEBSITE VIEWS
# ─────────────────────────────────────────────────────────────

def home(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('home'))
    ctx['banner']       = Banner.objects.first()
    ctx['services']     = Service.objects.all()
    ctx['ozbix_folios'] = OzbixFolio.objects.all()
    ctx['clients']      = Client.objects.all()
    ctx['testimonials'] = Testimonial.objects.filter(is_active=True)
    return render(request, 'index.html', ctx)


def shopify(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('shopify'))
    return render(request, 'shopify.html', ctx)


def wordpress(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('wordpress'))
    return render(request, 'wordpress.html', ctx)


def ecommerce(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('ecommerce'))
    return render(request, 'e-commerce.html', ctx)


def webdesign(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('webdesign'))
    return render(request, 'web-design.html', ctx)


def portfolio(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('portfolio'))
    ctx['ozbix_folios'] = OzbixFolio.objects.all()
    return render(request, 'portfolio.html', ctx)


def marketing(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('marketing'))
    return render(request, 'marketing.html', ctx)


def seo(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('seo'))
    return render(request, 'seo.html', ctx)


def graphic_design(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('graphic_design'))
    return render(request, 'graphic-design.html', ctx)


def other_services(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('other_services'))
    return render(request, 'other-services.html', ctx)


def software_services(request):
    ctx = _get_site_ctx()
    ctx.update(_page_ctx('software_services'))
    return render(request, 'software-services.html', ctx)


def contact(request):
    if request.method == 'POST':
        full_name     = request.POST.get('full_name', '').strip()
        email         = request.POST.get('email', '').strip()
        phone         = request.POST.get('phone', '').strip()
        service_list  = request.POST.getlist('services')
        message_text  = request.POST.get('message', '').strip()
        services_text = ', '.join(service_list) if service_list else 'General Inquiry'

        # 1. Save to database (so inquiries are NEVER lost)
        submission = ContactSubmission.objects.create(
            full_name=full_name or 'Anonymous',
            email=email or 'no-email@provided.com',
            phone=phone,
            services=services_text,
            message=message_text,
        )

        # 2. Prepare email parameters
        recipient = getattr(django_settings, 'EMAIL_ADMIN_RECIPIENT', None) or getattr(django_settings, 'EMAIL_HOST_USER', 'khudashkhan489@gmail.com')
        from_addr = getattr(django_settings, 'DEFAULT_FROM_EMAIL', None) or getattr(django_settings, 'EMAIL_HOST_USER', 'khudashkhan489@gmail.com')

        try:
            send_mail(
                subject=f'New Website Inquiry #{submission.id} - {full_name or "Anonymous"}',
                message=(
                    f"New Inquiry Received from Ozbix Website:\n\n"
                    f"Client Name:    {full_name}\n"
                    f"Email:          {email}\n"
                    f"Phone/WhatsApp: {phone}\n"
                    f"Services:       {services_text}\n\n"
                    f"Message:\n{message_text}\n\n"
                    f"-----------------------------------------\n"
                    f"View all inquiries in Admin Dashboard:\n"
                    f"http://127.0.0.1:8000/dashboard/messages/\n"
                ),
                from_email=from_addr,
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"[EMAIL SEND ERROR] Failed sending to {recipient}: {e}")
            print(f"[EMAIL SEND ERROR] {e}")

        messages.success(request, 'Shukriya! Aap ka message mil gaya, hum jald raabta karein ge.')
        return redirect('home')

    return redirect('home')


# ─────────────────────────────────────────────────────────────
# CUSTOM ADMIN DASHBOARD VIEWS
# ─────────────────────────────────────────────────────────────

def dashboard_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_index')
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect('dashboard_index')
        messages.error(request, 'Username ya password galat hai.')
    return render(request, 'dashboard/login.html')


def dashboard_logout_view(request):
    logout(request)
    return redirect('dashboard_login')


def _dash_base_ctx(page_title='Dashboard'):
    db = django_settings.DATABASES['default']
    return {
        'page_title':   page_title,
        'active_db':    getattr(django_settings, 'ACTIVE_DB_NAME', 'PostgreSQL'),
        'is_postgres':  True,
        'unread_count': ContactSubmission.objects.filter(is_read=False).count(),
    }


@login_required
def dashboard_index(request):
    ctx = _dash_base_ctx('Dashboard Overview')
    ctx.update({
        'services_count':  Service.objects.count(),
        'portfolio_count': OzbixFolio.objects.count(),
        'clients_count':   Client.objects.count(),
        'banners_count':   Banner.objects.count(),
        'messages_count':  ContactSubmission.objects.count(),
        'testimonials_count': Testimonial.objects.count(),
        'recent_inquiries': ContactSubmission.objects.all()[:6],
    })
    return render(request, 'dashboard/index.html', ctx)


@login_required
def dashboard_services(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Service.objects.create(
                icon_class=request.POST.get('icon_class', 'fas fa-concierge-bell'),
                title=request.POST.get('title', ''),
                short_description=request.POST.get('short_description', ''),
                description=request.POST.get('description', ''),
                button_text=request.POST.get('button_text', 'Read More'),
            )
            messages.success(request, 'Nayi service add kar di gayi!')
        elif action == 'edit':
            s = get_object_or_404(Service, id=request.POST.get('service_id'))
            s.icon_class        = request.POST.get('icon_class', s.icon_class)
            s.title             = request.POST.get('title', s.title)
            s.short_description = request.POST.get('short_description', s.short_description)
            s.description       = request.POST.get('description', s.description)
            s.button_text       = request.POST.get('button_text', s.button_text)
            s.save()
            messages.success(request, 'Service update ho gayi!')
        elif action == 'delete':
            get_object_or_404(Service, id=request.POST.get('service_id')).delete()
            messages.success(request, 'Service delete ho gayi!')
        return redirect('dashboard_services')

    ctx = _dash_base_ctx('Services Management')
    ctx['services'] = Service.objects.all()
    return render(request, 'dashboard/services.html', ctx)


@login_required
def dashboard_portfolio(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            img = request.FILES.get('image')
            if img:
                OzbixFolio.objects.create(title=request.POST.get('title', 'Project'), image=img)
                messages.success(request, 'Portfolio project add ho gaya!')
            else:
                messages.error(request, 'Image select karein.')
        elif action == 'delete':
            get_object_or_404(OzbixFolio, id=request.POST.get('item_id')).delete()
            messages.success(request, 'Portfolio item delete ho gaya!')
        return redirect('dashboard_portfolio')

    ctx = _dash_base_ctx('Portfolio Management')
    ctx['folios'] = OzbixFolio.objects.all()
    return render(request, 'dashboard/portfolio.html', ctx)


@login_required
def dashboard_banners(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            img = request.FILES.get('image')
            if img:
                Banner.objects.create(image=img)
                messages.success(request, 'Banner upload ho gaya!')
            else:
                messages.error(request, 'Image file select karein.')
        elif action == 'delete':
            get_object_or_404(Banner, id=request.POST.get('banner_id')).delete()
            messages.success(request, 'Banner delete ho gaya!')
        return redirect('dashboard_banners')

    ctx = _dash_base_ctx('Banner Management')
    ctx['banners'] = Banner.objects.all()
    return render(request, 'dashboard/banners.html', ctx)


@login_required
def dashboard_clients(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            img = request.FILES.get('image')
            if img:
                Client.objects.create(image=img)
                messages.success(request, 'Client logo upload ho gaya!')
            else:
                messages.error(request, 'Logo image select karein.')
        elif action == 'delete':
            get_object_or_404(Client, id=request.POST.get('client_id')).delete()
            messages.success(request, 'Client logo delete ho gaya!')
        return redirect('dashboard_clients')

    ctx = _dash_base_ctx('Client Logos')
    ctx['clients'] = Client.objects.all()
    return render(request, 'dashboard/clients.html', ctx)


@login_required
def dashboard_messages(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'test_email':
            target_addr = request.POST.get('test_email_address', '').strip() or getattr(django_settings, 'EMAIL_HOST_USER', '')
            try:
                send_mail(
                    subject='Ozbix Website - SMTP Connection Test',
                    message=(
                        'Assalam-o-Alaikum,\n\n'
                        'This is a confirmation test email from your Ozbix IT Solutions web application.\n'
                        'If you received this message, your Gmail SMTP connection, authentication, and App Password are functioning 100% properly!\n\n'
                        'Sender: ' + str(django_settings.DEFAULT_FROM_EMAIL) + '\n'
                        'Recipient: ' + target_addr + '\n\n'
                        'Ozbix Development House'
                    ),
                    from_email=django_settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[target_addr],
                    fail_silently=False,
                )
                messages.success(request, f'Test email kamyabi se bhej diya gaya: {target_addr}! Inbox ya Spam check karein.')
            except Exception as e:
                messages.error(request, f'Email send nahi ho saka: {e}')
            return redirect('dashboard_messages')

        sub = get_object_or_404(ContactSubmission, id=request.POST.get('msg_id'))
        if action == 'toggle_read':
            sub.is_read = not sub.is_read
            sub.save()
            messages.success(request, f"Message {'read' if sub.is_read else 'unread'} mark ho gaya.")
        elif action == 'delete':
            sub.delete()
            messages.success(request, 'Message delete ho gaya!')
        elif action == 'reply':
            try:
                send_mail(
                    subject=request.POST.get('reply_subject', 'Re: Your Inquiry'),
                    message=request.POST.get('reply_body', ''),
                    from_email=django_settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[sub.email],
                    fail_silently=False,
                )
                messages.success(request, f'Reply bhej di gayi — {sub.email}')
            except Exception as e:
                messages.error(request, f'Email send nahi ho saka: {e}')
        return redirect('dashboard_messages')

    ctx = _dash_base_ctx('Inquiries & Messages')
    ctx['submissions'] = ContactSubmission.objects.all()
    ctx['email_host_user'] = getattr(django_settings, 'EMAIL_HOST_USER', '')
    return render(request, 'dashboard/messages.html', ctx)


@login_required
def dashboard_testimonials(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Testimonial.objects.create(
                client_name=request.POST.get('client_name', ''),
                company=request.POST.get('company', ''),
                country=request.POST.get('country', ''),
                message=request.POST.get('message', ''),
                rating=int(request.POST.get('rating', 5)),
                avatar=request.FILES.get('avatar'),
            )
            messages.success(request, 'Testimonial add ho gaya!')
        elif action == 'delete':
            get_object_or_404(Testimonial, id=request.POST.get('t_id')).delete()
            messages.success(request, 'Testimonial delete ho gaya!')
        elif action == 'toggle':
            t = get_object_or_404(Testimonial, id=request.POST.get('t_id'))
            t.is_active = not t.is_active
            t.save()
            messages.success(request, 'Testimonial status update ho gaya!')
        return redirect('dashboard_testimonials')

    ctx = _dash_base_ctx('Testimonials Management')
    ctx['testimonials'] = Testimonial.objects.all()
    return render(request, 'dashboard/testimonials.html', ctx)


@login_required
def dashboard_page_heroes(request):
    if request.method == 'POST':
        action  = request.POST.get('action')
        page_id = request.POST.get('hero_id')
        if action == 'add':
            PageHero.objects.update_or_create(
                page=request.POST.get('page'),
                defaults={
                    'heading':     request.POST.get('heading', ''),
                    'subheading':  request.POST.get('subheading', ''),
                    'description': request.POST.get('description', ''),
                    'button_text': request.POST.get('button_text', 'Get Started'),
                    'button_link': request.POST.get('button_link', '#'),
                    'image':       request.FILES.get('image') or None,
                    'is_active':   True,
                }
            )
            messages.success(request, 'Page hero save ho gaya!')
        elif action == 'delete':
            get_object_or_404(PageHero, id=page_id).delete()
            messages.success(request, 'Page hero delete ho gaya!')
        elif action == 'toggle':
            h = get_object_or_404(PageHero, id=page_id)
            h.is_active = not h.is_active
            h.save()
            messages.success(request, 'Hero status update ho gaya!')
        return redirect('dashboard_page_heroes')

    ctx = _dash_base_ctx('Page Heroes Management')
    ctx['heroes'] = PageHero.objects.all()
    ctx['page_choices'] = PageHero.PAGE_CHOICES
    return render(request, 'dashboard/page_heroes.html', ctx)


@login_required
def dashboard_site_settings(request):
    site = SiteSettings.get_settings()
    if request.method == 'POST':
        site.site_name          = request.POST.get('site_name', site.site_name)
        site.tagline            = request.POST.get('tagline', site.tagline)
        site.email              = request.POST.get('email', site.email)
        site.phone_pk           = request.POST.get('phone_pk', site.phone_pk)
        site.phone_uae          = request.POST.get('phone_uae', site.phone_uae)
        site.phone_au           = request.POST.get('phone_au', site.phone_au)
        site.whatsapp_number    = request.POST.get('whatsapp_number', site.whatsapp_number)
        site.facebook_url       = request.POST.get('facebook_url', site.facebook_url)
        site.instagram_url      = request.POST.get('instagram_url', site.instagram_url)
        site.twitter_url        = request.POST.get('twitter_url', site.twitter_url)
        site.linkedin_url       = request.POST.get('linkedin_url', site.linkedin_url)
        site.address            = request.POST.get('address', site.address)
        site.footer_description = request.POST.get('footer_description', site.footer_description)
        if request.FILES.get('logo'):
            site.logo = request.FILES['logo']
        site.save()
        messages.success(request, 'Site settings save ho gayi!')
        return redirect('dashboard_site_settings')

    ctx = _dash_base_ctx('Site Settings')
    ctx['site_obj'] = site
    return render(request, 'dashboard/site_settings.html', ctx)


@login_required
def dashboard_db_status(request):
    sql_path    = os.path.join(django_settings.BASE_DIR, 'postgray.sql')
    sql_content = ''
    if os.path.exists(sql_path):
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
    ctx = _dash_base_ctx('PostgreSQL & DB Setup')
    ctx.update({
        'db_config':   django_settings.DATABASES['default'],
        'sql_content': sql_content,
    })
    return render(request, 'dashboard/db_settings.html', ctx)


@login_required
def dashboard_account(request):
    user = request.user
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            user.username   = request.POST.get('username', user.username).strip()
            user.email      = request.POST.get('email', user.email).strip()
            user.first_name = request.POST.get('first_name', user.first_name).strip()
            user.last_name  = request.POST.get('last_name', user.last_name).strip()
            user.save()
            messages.success(request, 'Admin profile successfully update ho gaya!')
        elif action == 'change_password':
            old_pass     = request.POST.get('old_password')
            new_pass     = request.POST.get('new_password')
            confirm_pass = request.POST.get('confirm_password')
            if not user.check_password(old_pass):
                messages.error(request, 'Purana password ghalat hai.')
            elif not new_pass or len(new_pass) < 4:
                messages.error(request, 'Naya password kam az kam 4 characters ka hona chahiye.')
            elif new_pass != confirm_pass:
                messages.error(request, 'Dono naye passwords aapas me match nahi karte.')
            else:
                user.set_password(new_pass)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password kamyabi se tabdeel ho gaya!')
        return redirect('dashboard_account')

    ctx = _dash_base_ctx('Admin Account & Security')
    return render(request, 'dashboard/account.html', ctx)