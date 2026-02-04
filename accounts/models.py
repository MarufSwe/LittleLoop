from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile for LittleLoop users.
    Stores additional information beyond Django's default User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile fields
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True, help_text="City or area")
    bio = models.TextField(blank=True, help_text="Brief description about yourself")
    
    # Profile completion status
    is_complete = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def mark_complete(self):
        """Mark profile as complete if all required fields are filled"""
        self.is_complete = bool(
            self.full_name and 
            self.phone_number and 
            self.location
        )
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created.
    This ensures every user has a profile.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the user's profile whenever the user is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
