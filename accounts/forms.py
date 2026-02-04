from django import forms
from .models import UserProfile


class ProfileCompletionForm(forms.ModelForm):
    """
    Form for completing user profile after social login.
    Validates and saves profile information.
    """
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'full_name', 'phone_number', 'location', 'bio']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'required': True,
                'type': 'tel'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Dhaka, Bangladesh',
                'required': True
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us a little about yourself...',
                'rows': 4
            }),
        }
        labels = {
            'profile_picture': 'Profile Picture (Optional)',
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'location': 'Location (City/Area)',
            'bio': 'About You (Optional)',
        }
    
    def clean_phone_number(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone_number')
        if phone and len(phone) < 10:
            raise forms.ValidationError("Please enter a valid phone number")
        return phone
