"""
URL configuration for accounts app (authentication & profile management)
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Profile completion page (redirected after first login)
    path('complete/', views.profile_complete, name='profile_complete'),
]
