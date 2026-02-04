"""
Middleware for checking user profile completion status.

This middleware will be expanded in STEP 3 - User Profile & Mandatory Completion.
For now, it's a placeholder that demonstrates the structure.
"""

from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    """
    Middleware to check if authenticated users have completed their profile.
    
    After social login, users should be redirected to profile completion page
    if their profile is incomplete.
    
    This will be fully implemented in STEP 3.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that should be accessible without profile completion
        self.exempt_urls = [
            '/accounts/',  # Allauth URLs (login, logout, etc.)
            '/profile/complete/',  # Profile completion page itself
            '/admin/',  # Django admin
            '/static/',  # Static files
            '/media/',  # Media files
        ]
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        This method will be called before Django calls the view.
        
        In STEP 3, we'll add logic to:
        1. Check if user is authenticated
        2. Check if user has completed profile (using UserProfile model)
        3. Redirect to profile completion if needed
        4. Allow access to exempt URLs
        
        Example logic for STEP 3:
        
        if request.user.is_authenticated:
            # Skip check for exempt URLs
            for url in self.exempt_urls:
                if request.path.startswith(url):
                    return None
            
            # Check if user has completed profile
            try:
                profile = request.user.profile
                if not profile.is_complete:
                    return redirect(reverse('accounts:profile_complete'))
            except UserProfile.DoesNotExist:
                return redirect(reverse('accounts:profile_complete'))
        
        return None
        """
        # Placeholder - will be implemented in STEP 3
        return None
