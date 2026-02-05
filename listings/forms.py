from django import forms
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
            'price', 'area'
        ]
        widgets = {
            'item_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_item_type',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Blue Cotton Onesie for Baby Boy',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the condition, brand, features, etc.',
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
                'placeholder': 'e.g., 6M, 12M, 2T',
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_price',
                'placeholder': 'Enter amount in BDT',
                'min': '0',
                'step': '0.01',
            }),
            'area': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Dhanmondi, Dhaka',
            }),
        }
        labels = {
            'item_type': 'What do you want to do?',
            'title': 'Item Title',
            'description': 'Description',
            'image1': 'Upload Image 1 (Primary)',
            'image2': 'Upload Image 2 (Optional)',
            'image3': 'Upload Image 3 (Optional)',
            'baby_gender': 'Gender',
            'age_range': 'Age Range',
            'size': 'Size',
            'condition': 'Condition',
            'price': 'Price (BDT)',
            'area': 'Your Area/Location',
        }
    
    def clean(self):
        """
        Custom validation:
        - Price is required for 'sell' items
        - Price should be None for 'donate' items
        """
        cleaned_data = super().clean()
        item_type = cleaned_data.get('item_type')
        price = cleaned_data.get('price')
        
        if item_type == 'sell' and not price:
            self.add_error('price', 'Price is required for selling items.')
        
        if item_type == 'donate' and price:
            cleaned_data['price'] = None  # Ignore price for donate items
        
        return cleaned_data
