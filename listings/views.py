from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Item
from .forms import ItemForm


def item_list(request):
    """
    Public homepage showing all available items (donate/sell).
    No login required - anyone can browse.
    Supports filtering via GET parameters.
    """
    # Get all available items
    items = Item.objects.filter(status='available').select_related('owner__profile')
    
    # Apply filters from GET parameters
    item_type = request.GET.get('type')
    gender = request.GET.get('gender')
    age_range = request.GET.get('age')
    area = request.GET.get('area')
    
    if item_type:
        items = items.filter(item_type=item_type)
    if gender:
        items = items.filter(baby_gender=gender)
    if age_range:
        items = items.filter(age_range=age_range)
    if area:
        items = items.filter(area__icontains=area)
    
    # Get filter options for the UI
    context = {
        'items': items,
        'selected_type': item_type,
        'selected_gender': gender,
        'selected_age': age_range,
        'selected_area': area,
        'item_type_choices': Item.ITEM_TYPE_CHOICES,
        'gender_choices': Item.GENDER_CHOICES,
        'age_range_choices': Item.AGE_RANGE_CHOICES,
    }
    
    return render(request, 'listings/item_list.html', context)


def item_detail(request, pk):
    """
    Public detail view for an item.
    Shows full details and collect/buy button (login required for action).
    """
    item = get_object_or_404(Item, pk=pk)
    
    # Check if user is authenticated and has completed profile
    show_contact = False
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_complete:
        show_contact = True
    
    context = {
        'item': item,
        'show_contact': show_contact,
    }
    
    return render(request, 'listings/item_detail.html', context)


@login_required
def item_create(request):
    """
    Create new item (donate or sell).
    Requires login and profile completion.
    """
    # Check if profile is complete
    if not hasattr(request.user, 'profile') or not request.user.profile.is_complete:
        messages.warning(request, _('Please complete your profile first.'))
        return redirect('accounts:profile_complete')
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            
            messages.success(request, _('Your item "%(title)s" has been posted successfully!') % {'title': item.title})
            return redirect('listings:item_detail', pk=item.pk)
    else:
        form = ItemForm()
    
    context = {
        'form': form,
        'is_edit': False,
    }
    
    return render(request, 'listings/item_create.html', context)


@login_required
def item_edit(request, pk):
    """
    Edit existing item.
    Only owner can edit their own items.
    Can only edit items that are still 'available'.
    """
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    
    # Prevent editing of 'done' items
    if item.status == 'done':
        messages.error(request, _('Cannot edit items that are marked as done.'))
        return redirect('listings:my_items')
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, _('"%s" has been updated successfully!') % item.title)
            return redirect('listings:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
        'is_edit': True,
    }
    
    return render(request, 'listings/item_create.html', context)


@login_required
def my_items(request):
    """
    List all items created by the logged-in user.
    Allows marking items as done.
    """
    items = Item.objects.filter(owner=request.user).order_by('-created_at')
    
    # Count items by status
    available_count = items.filter(status='available').count()
    done_count = items.filter(status='done').count()
    
    context = {
        'items': items,
        'available_count': available_count,
        'done_count': done_count,
    }
    
    return render(request, 'listings/my_items.html', context)


@login_required
def item_mark_done(request, pk):
    """
    Mark an item as done (no longer available).
    Only owner can mark their own items as done.
    """
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        item.mark_done()
        messages.success(request, _('"%s" marked as done.') % item.title)
    
    return redirect('listings:my_items')
