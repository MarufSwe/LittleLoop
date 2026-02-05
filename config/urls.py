"""
URL configuration for LittleLoop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # Homepage - Public item listings
    path('', include('listings.urls')),
    
    # Django Allauth URLs (handles login, logout, social auth)
    path('accounts/', include('allauth.urls')),
    
    # Custom accounts app URLs (profile completion, etc.)
    path('profile/', include('accounts.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
