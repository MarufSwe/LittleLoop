from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrPhoneBackend(ModelBackend):
    """
    Custom authentication backend that allows login with email or phone number.
    Phone numbers are stored in username field with 'phone_' prefix.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # Check if input is email or phone
            if '@' in username:
                # Email login
                user = User.objects.get(email=username)
            else:
                # Phone login - stored as username with 'phone_' prefix
                user = User.objects.get(username=f'phone_{username}')
            
            # Check password
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
