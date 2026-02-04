"""
URL configuration for accounts app (authentication & profile management)
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Profile completion page (redirected after first login)
    path('complete/', views.profile_complete, name='profile_complete'),
    
    # Profile view page
    path('profile/', views.profile_view, name='profile_view'),
    
    # History page
    path('history/', views.history_view, name='history'),
]
