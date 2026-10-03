from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def home_status(request):
    return JsonResponse({
        "status": "online",
        "service": "SmartExams Backend API",
        "version": "1.0",
        "endpoints": {
            "api_root": "/api/",
            "auth_token": "/api/auth/token/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('', home_status, name='home_status'),
    path('admin/', admin.site.super_user if hasattr(admin.site, 'super_user') else admin.site.urls),
    path('api/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
