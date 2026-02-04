from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def profile_complete(request):
    """
    View for completing user profile after social login.
    This will be expanded in STEP 3 - User Profile & Mandatory Completion.
    
    For now, it's a placeholder that shows a message.
    """
    return render(request, 'accounts/profile_complete.html')
