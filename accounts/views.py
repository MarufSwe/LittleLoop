from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileCompletionForm
from .models import UserProfile


@login_required
def profile_complete(request):
    """
    View for completing user profile after social login.
    
    GET: Display the profile completion form (pre-filled with existing data)
    POST: Save the profile data and mark as complete
    """
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Pre-fill full_name from user's first/last name or email
    if not profile.full_name and request.user.first_name:
        profile.full_name = f"{request.user.first_name} {request.user.last_name}".strip()
    
    if request.method == 'POST':
        form = ProfileCompletionForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the profile
            profile = form.save(commit=False)
            profile.mark_complete()  # Mark as complete and save
            
            messages.success(request, 'Profile completed successfully! Welcome to LittleLoop.')
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileCompletionForm(instance=profile)
    
    return render(request, 'accounts/profile_complete.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def profile_view(request):
    """View user profile"""
    profile = request.user.profile
    return render(request, 'accounts/profile_view.html', {'profile': profile})


@login_required
def history_view(request):
    """View user's donation/sale/purchase history"""
    # This will be implemented when we add listings functionality
    return render(request, 'accounts/history.html')
