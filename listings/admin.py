from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Admin interface for Item model"""
    
    list_display = ['id', 'title', 'owner', 'item_type', 'baby_gender', 'age_range', 
                    'area', 'price', 'status', 'created_at']
    list_filter = ['item_type', 'baby_gender', 'age_range', 'condition', 'status', 'created_at']
    search_fields = ['title', 'description', 'area', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Owner', {
            'fields': ('owner',)
        }),
        ('Item Information', {
            'fields': ('item_type', 'title', 'description', 'image1', 'image2', 'image3')
        }),
        ('Baby Details', {
            'fields': ('baby_gender', 'age_range', 'size', 'condition')
        }),
        ('Location & Pricing', {
            'fields': ('area', 'detailed_address', 'price')
        }),
        ('Alternative Contact (Optional)', {
            'fields': ('use_alternative_contact', 'alternative_contact_name', 'alternative_contact_phone'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Auto-set owner if not set"""
        if not obj.pk:  # New object
            if not obj.owner_id:
                obj.owner = request.user
        super().save_model(request, obj, form, change)
