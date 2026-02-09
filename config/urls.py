"""
URL configuration for LittleLoop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # Language switcher
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Homepage - Public item listings
    path('', include('listings.urls')),
    
    # Profile management (no login required - direct to profile)
    path('profile/', include('accounts.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
