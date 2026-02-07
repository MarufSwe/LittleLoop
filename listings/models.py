from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Item(models.Model):
    """
    Model for baby clothes listings (donate or sell).
    """
    
    # Item type choices
    ITEM_TYPE_CHOICES = [
        ('donate', _('Donate')),
        ('sell', _('Sell')),
    ]
    
    # Gender choices
    GENDER_CHOICES = [
        ('boy', _('Boy')),
        ('girl', _('Girl')),
        ('unisex', _('Unisex')),
    ]
    
    # Age range choices
    AGE_RANGE_CHOICES = [
        ('0-3m', _('0-3 months')),
        ('3-6m', _('3-6 months')),
        ('6-12m', _('6-12 months')),
        ('1-2y', _('1-2 years')),
        ('2-3y', _('2-3 years')),
        ('3-4y', _('3-4 years')),
        ('4-5y', _('4-5 years')),
        ('5+y', _('5+ years')),
    ]
    
    # Condition choices
    CONDITION_CHOICES = [
        ('new', _('Like New')),
        ('excellent', _('Excellent')),
        ('good', _('Good')),
        ('fair', _('Fair')),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('available', _('Available')),
        ('done', _('Done')),
    ]
    
    # Area/Location choices (Dhaka areas)
    AREA_CHOICES = [
        ('mirpur', _('Mirpur')),
        ('mohammadpur', _('Mohammadpur')),
        ('uttara', _('Uttara')),
        ('dhanmondi', _('Dhanmondi')),
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
    
    # Location (dropdown + detailed address)
    area = models.CharField(max_length=50, choices=AREA_CHOICES, help_text="Select your area")
    detailed_address = models.CharField(max_length=255, blank=True, 
                                        help_text="e.g., Road 01, House 20, Block A")
    
    # Alternative Contact (Optional - for privacy or convenience)
    use_alternative_contact = models.BooleanField(default=False, 
                                                   help_text="Use different contact for this item")
    alternative_contact_name = models.CharField(max_length=100, blank=True,
                                                help_text="e.g., Guard, House Helper, Family Member")
    alternative_contact_phone = models.CharField(max_length=20, blank=True,
                                                 help_text="Alternative phone number")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['-created_at']  # Newest first
    
    def compress_image(self, image_field):
        """
        Compress image to reduce file size while maintaining quality.
        Target: Reduce 5MB images to ~100-200KB
        """
        if not image_field:
            return None
        
        # Open the image
        img = Image.open(image_field)
        
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize if image is too large (max 1200px on longest side)
        max_size = 1200
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Compress and save to BytesIO
        output = BytesIO()
        img.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        # Create new InMemoryUploadedFile
        compressed_image = InMemoryUploadedFile(
            output, 'ImageField',
            f"{image_field.name.split('.')[0]}.jpg",
            'image/jpeg',
            sys.getsizeof(output), None
        )
        
        return compressed_image
    
    def save(self, *args, **kwargs):
        """
        Override save to compress images before saving
        """
        # Compress each image if it exists and is new
        if self.image1 and not self.pk:  # New upload
            self.image1 = self.compress_image(self.image1)
        elif self.image1 and self.pk:  # Check if image changed
            try:
                old_item = Item.objects.get(pk=self.pk)
                if old_item.image1 != self.image1:
                    self.image1 = self.compress_image(self.image1)
            except Item.DoesNotExist:
                pass
        
        if self.image2:
            try:
                if not self.pk or Item.objects.get(pk=self.pk).image2 != self.image2:
                    self.image2 = self.compress_image(self.image2)
            except Item.DoesNotExist:
                self.image2 = self.compress_image(self.image2)
        
        if self.image3:
            try:
                if not self.pk or Item.objects.get(pk=self.pk).image3 != self.image3:
                    self.image3 = self.compress_image(self.image3)
            except Item.DoesNotExist:
                self.image3 = self.compress_image(self.image3)
        
        super().save(*args, **kwargs)
    
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
