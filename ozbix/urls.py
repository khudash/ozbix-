
from django.shortcuts import redirect
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

def redirect_to_dashboard(request):
    return redirect('dashboard_index')

urlpatterns = [
    # Built-in Django admin panel removed — all dynamic controls handled via custom dashboard
    path('admin/', redirect_to_dashboard, name='admin_redirect'),
    path('admin', redirect_to_dashboard),
    path("", include("website.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)