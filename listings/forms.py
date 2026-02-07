from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Item


class ItemForm(forms.ModelForm):
    """
    Form for creating/editing baby clothes items (donate or sell).
    """
    
    class Meta:
        model = Item
        fields = [
            'item_type', 'title', 'description', 'image1', 'image2', 'image3',
            'baby_gender', 'age_range', 'size', 'condition',
            'price', 'area', 'detailed_address',
            'use_alternative_contact', 'alternative_contact_name', 'alternative_contact_phone'
        ]
        widgets = {
            'item_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_item_type',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Blue Cotton Shirt for Baby Boy'),
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Describe the condition, brand, features, etc.'),
            }),
            'image1': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'id_image1',
            }),
            'image2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'id_image2',
            }),
            'image3': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'id_image3',
            }),
            'baby_gender': forms.Select(attrs={
                'class': 'form-select',
            }),
            'age_range': forms.Select(attrs={
                'class': 'form-select',
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., 6M, 12M, 2T'),
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_price',
                'placeholder': _('Enter amount in BDT'),
                'min': '0',
                'step': '0.01',
            }),
            'area': forms.Select(attrs={
                'class': 'form-select',
            }),
            'detailed_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Road 01, House 20, Block A (Optional)'),
            }),
            'use_alternative_contact': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_use_alternative_contact',
            }),
            'alternative_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Guard, House Helper, Family Member'),
            }),
            'alternative_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., 01712345678'),
            }),
        }
        labels = {
            'item_type': _('What do you want to do?'),
            'title': _('Item Title'),
            'description': _('Description'),
            'image1': _('Upload Image 1 (Required)'),
            'image2': _('Upload Image 2 (Optional)'),
            'image3': _('Upload Image 3 (Optional)'),
            'baby_gender': _('Gender'),
            'age_range': _('Age Range'),
            'size': _('Size'),
            'condition': _('Condition'),
            'price': _('Price (BDT)'),
            'area': _('Select Area'),
            'detailed_address': _('Detailed Address (Optional)'),
            'use_alternative_contact': _('Use Alternative Contact?'),
            'alternative_contact_name': _('Contact Person Name'),
            'alternative_contact_phone': _('Alternative Phone Number'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image1 required
        self.fields['image1'].required = True
    
    def clean(self):
        """
        Custom validation:
        - Require price for 'sell' items
        - Ensure price is empty/null for 'donate' items
        - Require alternative contact details if checkbox is checked
        """
        cleaned_data = super().clean()
        item_type = cleaned_data.get('item_type')
        price = cleaned_data.get('price')
        
        # Price validation
        if item_type == 'sell' and not price:
            self.add_error('price', 'Price is required for selling items.')
        
        if item_type == 'donate' and price:
            cleaned_data['price'] = None  # Ignore price for donate items
        
        # Alternative contact validation
        use_alt_contact = cleaned_data.get('use_alternative_contact')
        alt_name = cleaned_data.get('alternative_contact_name')
        alt_phone = cleaned_data.get('alternative_contact_phone')
        
        if use_alt_contact:
            if not alt_name:
                self.add_error('alternative_contact_name', _('Contact person name is required.'))
            if not alt_phone:
                self.add_error('alternative_contact_phone', _('Alternative phone number is required.'))
        
        return cleaned_data
