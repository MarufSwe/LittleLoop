from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    # Public item list (homepage)
    path('', views.item_list, name='item_list'),
    
    # Item detail (public)
    path('<int:pk>/', views.item_detail, name='item_detail'),
    
    # Create item (login required)
    path('create/', views.item_create, name='item_create'),
    
    # Edit item (login required)
    path('<int:pk>/edit/', views.item_edit, name='item_edit'),
    
    # My items (login required)
    path('my-items/', views.my_items, name='my_items'),
    
    # Mark item as done (login required)
    path('<int:pk>/mark-done/', views.item_mark_done, name='item_mark_done'),
]
