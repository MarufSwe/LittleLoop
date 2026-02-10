from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import UserProfile
import re


class SignupForm(forms.Form):
    """
    Signup form with email/phone + password.
    Users can choose to signup with either email or phone.
    """
    login_type = forms.ChoiceField(
        choices=[('email', _('Email')), ('phone', _('Phone Number'))],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label=_('Login with'),
        initial='phone'
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email'),
        }),
        label=_('Email Address')
    )
    
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('01XXXXXXXXX'),
            'maxlength': '11',
            'pattern': '^01[0-9]{9}$'
        }),
        label=_('Phone Number (BD)')
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Create a password'),
        }),
        label=_('Password'),
        min_length=6
    )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm your password'),
        }),
        label=_('Confirm Password')
    )
    
    def clean_phone(self):
        """Validate Bangladeshi phone number format"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove spaces and dashes
            phone = re.sub(r'[\s\-]', '', phone)
            
            # Check if it's 11 digits starting with 01
            if not re.match(r'^01[0-9]{9}$', phone):
                raise ValidationError(_('Please enter a valid BD phone number (11 digits, starting with 01)'))
            
            # Check if phone already exists
            if User.objects.filter(username=f'phone_{phone}').exists():
                raise ValidationError(_('This phone number is already registered'))
        
        return phone
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already registered'))
        return email
    
    def clean(self):
        """Validate that either email or phone is provided and passwords match"""
        cleaned_data = super().clean()
        login_type = cleaned_data.get('login_type')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Check login type (only if field doesn't already have errors)
        if login_type == 'email' and not email and 'email' not in self.errors:
            raise ValidationError(_('Email is required when using email login'))
        
        if login_type == 'phone' and not phone and 'phone' not in self.errors:
            raise ValidationError(_('Phone number is required when using phone login'))
        
        # Check password match
        if password and password_confirm and password != password_confirm:
            raise ValidationError(_('Passwords do not match'))
        
        return cleaned_data


class LoginForm(forms.Form):
    """
    Login form that accepts email or phone number + password.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email or Phone Number'),
        }),
        label=_('Email or Phone Number')
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password'),
        }),
        label=_('Password')
    )


class ProfileCompletionForm(forms.ModelForm):
    """
    Form for completing user profile after signup.
    Email or phone is excluded based on what user signed up with.
    """
    
    # Add email field for phone signups
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email address'),
        }),
        label=_('Email Address')
    )
    
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
                'placeholder': _('Enter your full name'),
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '01XXXXXXXXX',
                'required': True,
                'type': 'tel',
                'maxlength': '11',
                'pattern': '^01[0-9]{9}$'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Dhaka, Bangladesh'),
                'required': True
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Tell us a little about yourself...'),
                'rows': 4
            }),
        }
        labels = {
            'profile_picture': _('Profile Picture (Optional)'),
            'full_name': _('Full Name'),
            'phone_number': _('Phone Number'),
            'location': _('Location (City/Area)'),
            'bio': _('About You (Optional)'),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # If user signed up with phone, remove phone field and require email
        if self.user and self.user.username.startswith('phone_'):
            self.fields.pop('phone_number', None)
            self.fields['email'].required = True
            # Pre-populate email if it exists
            if self.user.email and not self.initial.get('email'):
                self.initial['email'] = self.user.email
        else:
            # If user signed up with email, remove email field
            self.fields.pop('email', None)
    
    def clean_phone_number(self):
        """Validate Bangladeshi phone number format (11 digits)"""
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove spaces and dashes
            phone = re.sub(r'[\s\-]', '', phone)
            
            # Check if it's 11 digits starting with 01
            if not re.match(r'^01[0-9]{9}$', phone):
                raise ValidationError(_('Please enter a valid BD phone number (11 digits, starting with 01)'))
        
        return phone
    
    def clean_email(self):
        """Validate email uniqueness for phone signups"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists (exclude current user)
            existing = User.objects.filter(email=email)
            if self.user:
                existing = existing.exclude(id=self.user.id)
            
            if existing.exists():
                raise ValidationError(_('This email is already registered'))
        return email
