from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    """
    Model for baby clothes listings (donate or sell).
    """
    
    # Item type choices
    ITEM_TYPE_CHOICES = [
        ('donate', 'Donate'),
        ('sell', 'Sell'),
    ]
    
    # Gender choices
    GENDER_CHOICES = [
        ('boy', 'Boy'),
        ('girl', 'Girl'),
        ('unisex', 'Unisex'),
    ]
    
    # Age range choices
    AGE_RANGE_CHOICES = [
        ('0-3m', '0-3 months'),
        ('3-6m', '3-6 months'),
        ('6-12m', '6-12 months'),
        ('1-2y', '1-2 years'),
        ('2-3y', '2-3 years'),
        ('3-4y', '3-4 years'),
        ('4-5y', '4-5 years'),
        ('5+y', '5+ years'),
    ]
    
    # Condition choices
    CONDITION_CHOICES = [
        ('new', 'Like New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('done', 'Done'),
    ]
    
    # Core fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    
    # Item details
    title = models.CharField(max_length=200)
    description = models.TextField()
    image1 = models.ImageField(upload_to='items/', blank=True, null=True, help_text="Primary image")
    image2 = models.ImageField(upload_to='items/', blank=True, null=True, help_text="Second image")
    image3 = models.ImageField(upload_to='items/', blank=True, null=True, help_text="Third image")
    
    # Baby info
    baby_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age_range = models.CharField(max_length=10, choices=AGE_RANGE_CHOICES)
    size = models.CharField(max_length=50, help_text="e.g., 6M, 12M, 2T")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, 
                                 help_text="Price in BDT (only for sell items)")
    
    # Location
    area = models.CharField(max_length=100, help_text="Area or location")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['-created_at']  # Newest first
    
    def __str__(self):
        return f"{self.title} - {self.get_item_type_display()}"
    
    def is_available(self):
        """Check if item is still available"""
        return self.status == 'available'
    
    def mark_done(self):
        """Mark item as done"""
        self.status = 'done'
        self.save()
    
    def get_primary_image(self):
        """Get the first available image"""
        return self.image1 or self.image2 or self.image3
    
    def get_all_images(self):
        """Get all uploaded images as a list"""
        images = []
        if self.image1:
            images.append(self.image1)
        if self.image2:
            images.append(self.image2)
        if self.image3:
            images.append(self.image3)
        return images
