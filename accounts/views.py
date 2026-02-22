from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _
from django.urls import reverse
from .forms import SignupForm, LoginForm, ProfileCompletionForm
from .models import UserProfile


def signup_view(request):
    """
    Signup view - create account with email/phone + password.
    After signup, redirect to profile completion.
    """
    if request.user.is_authenticated:
        # Already logged in, check profile
        if hasattr(request.user, 'profile') and request.user.profile.is_complete:
            return redirect('listings:item_list')
        else:
            return redirect('accounts:profile_complete')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            login_type = form.cleaned_data['login_type']
            password = form.cleaned_data['password']
            
            # Create user based on login type
            if login_type == 'email':
                email = form.cleaned_data['email']
                user = User.objects.create_user(
                    username=email,  # Use email as username
                    email=email,
                    password=password
                )
            else:  # phone
                phone = form.cleaned_data['phone']
                user = User.objects.create_user(
                    username=f'phone_{phone}',  # Prefix to identify phone users
                    password=password
                )
            
            # Login the user with explicit backend
            login(request, user, backend='accounts.backends.EmailOrPhoneBackend')
            messages.success(request, _('Account created successfully! Please complete your profile.'))
            return redirect('accounts:profile_complete')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """
    Login view - authenticate with email/phone + password.
    After login, redirect to profile completion if incomplete, else to 'next' or homepage.
    """
    # Get the 'next' parameter from GET or POST
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if request.user.is_authenticated:
        # Already logged in, check profile
        if hasattr(request.user, 'profile') and request.user.profile.is_complete:
            return redirect(next_url) if next_url else redirect('listings:item_list')
        else:
            return redirect('accounts:profile_complete')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate using custom backend
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Login with explicit backend
                login(request, user, backend='accounts.backends.EmailOrPhoneBackend')
                
                # Check if profile is complete
                if hasattr(user, 'profile') and user.profile.is_complete:
                    messages.success(request, _('Welcome back!'))
                    # Redirect to 'next' URL or homepage
                    return redirect(next_url) if next_url else redirect('listings:item_list')
                else:
                    messages.info(request, _('Please complete your profile'))
                    # Pass 'next' to profile completion
                    if next_url:
                        return redirect(f"{reverse('accounts:profile_complete')}?next={next_url}")
                    return redirect('accounts:profile_complete')
            else:
                messages.error(request, _('Invalid email/phone or password'))
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """Logout user and redirect to homepage"""
    logout(request)
    messages.success(request, _('You have been logged out successfully'))
    return redirect('listings:item_list')


def profile_complete(request):
    """
    View for completing user profile after signup.
    Excludes email if user signed up with email, excludes phone if signed up with phone.
    """
    # Get the 'next' parameter
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if not request.user.is_authenticated:
        messages.warning(request, _('Please login first'))
        return redirect('accounts:login')
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileCompletionForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            
            # If user signed up with phone, save phone to profile and email to user
            if request.user.username.startswith('phone_'):
                phone = request.user.username.replace('phone_', '')
                profile.phone_number = phone
                
                # Save email to user model
                email = form.cleaned_data.get('email')
                if email:
                    request.user.email = email
                    request.user.save()
            
            profile.mark_complete()  # Mark as complete and save
            
            messages.success(request, _('Profile completed successfully! Welcome to LittleLoop.'))
            # Redirect to 'next' URL or homepage
            return redirect(next_url) if next_url else redirect('listings:item_list')
    else:
        form = ProfileCompletionForm(instance=profile, user=request.user)
    
    return render(request, 'accounts/profile_complete.html', {
        'form': form,
        'profile': profile,
        'signed_up_with_phone': request.user.username.startswith('phone_'),
        'next': next_url,
    })


def profile_view(request):
    """View user profile"""
    if not request.user.is_authenticated:
        messages.warning(request, _('Please login first'))
        return redirect('accounts:login')
    
    if not hasattr(request.user, 'profile') or not request.user.profile.is_complete:
        messages.warning(request, _('Please complete your profile first'))
        return redirect('accounts:profile_complete')
    
    profile = request.user.profile
    return render(request, 'accounts/profile_view.html', {'profile': profile})


def history_view(request):
    """View user's donation/sale/purchase history"""
    if not request.user.is_authenticated:
        messages.warning(request, _('Please login first'))
        return redirect('accounts:login')
    
    # This will be implemented when we add listings functionality
    return render(request, 'accounts/history.html')
