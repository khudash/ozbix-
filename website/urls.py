from django.urls import path
from . import views

urlpatterns = [
    # ── Public Website ──────────────────────────────────────────
    path('',                    views.home,              name='home'),
    path('shopify/',            views.shopify,           name='shopify'),
    path('wordpress/',          views.wordpress,         name='wordpress'),
    path('ecommerce/',          views.ecommerce,         name='ecommerce'),
    path('webdesign/',          views.webdesign,         name='webdesign'),
    path('portfolio/',          views.portfolio,         name='portfolio'),
    path('marketing/',          views.marketing,         name='marketing'),
    path('seo/',                views.seo,               name='seo'),
    path('graphic-design/',     views.graphic_design,    name='graphic_design'),
    path('other-services/',     views.other_services,    name='other_services'),
    path('software-services/',  views.software_services, name='software_services'),
    path('contact/',            views.contact,           name='contact'),

    # ── Custom Dashboard ─────────────────────────────────────────
    path('dashboard/',                views.dashboard_index,          name='dashboard_index'),
    path('dashboard/login/',          views.dashboard_login_view,     name='dashboard_login'),
    path('dashboard/logout/',         views.dashboard_logout_view,    name='dashboard_logout'),
    path('dashboard/services/',       views.dashboard_services,       name='dashboard_services'),
    path('dashboard/portfolio/',      views.dashboard_portfolio,      name='dashboard_portfolio'),
    path('dashboard/banners/',        views.dashboard_banners,        name='dashboard_banners'),
    path('dashboard/clients/',        views.dashboard_clients,        name='dashboard_clients'),
    path('dashboard/messages/',       views.dashboard_messages,       name='dashboard_messages'),
    path('dashboard/testimonials/',   views.dashboard_testimonials,   name='dashboard_testimonials'),
    path('dashboard/page-heroes/',    views.dashboard_page_heroes,    name='dashboard_page_heroes'),
    path('dashboard/site-settings/',  views.dashboard_site_settings,  name='dashboard_site_settings'),
    path('dashboard/account/',        views.dashboard_account,        name='dashboard_account'),
    path('dashboard/db-status/',      views.dashboard_db_status,      name='dashboard_db_status'),
]