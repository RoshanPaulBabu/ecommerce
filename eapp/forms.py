from django import forms
from .models import Address
from django.core.validators import RegexValidator

class AddressForm(forms.ModelForm):
    # Define the RegexValidator for the recipient contact
    recipient_contact_validator = RegexValidator(
        regex=r'^\d{10,12}$',  # Only allow numeric characters with length between 10 and 12
        message='Recipient contact must be between 10 and 12 digits and contain only numbers.'
    )

    # Apply the validator to the recepient_contact field
    recepient_contact = forms.CharField(
        validators=[recipient_contact_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipient Contact'}),
        required=True
    )
    class Meta:
        model = Address
        fields = ['recepient_name', 'recepient_contact', 'address_line1', 'address_line2', 'city', 'state', 'postal_code']
        widgets = {
            'recepient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipient Name'}),
            'recepient_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipient Contact'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
        }
        
        
