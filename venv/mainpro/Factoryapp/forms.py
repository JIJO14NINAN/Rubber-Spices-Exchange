# FactoryApp/forms.py

from django import forms
from .models import Factory

class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = ['factoryName', 'location', 'owner', 'contact', 'email', 'license', 'type']
        widgets = {
            'factoryName': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'license': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'factoryName': 'Factory Name',
            'location': 'Location',
            'owner': 'Owner',
            'contact': 'Contact Number',
            'email': 'Email Address',
            'license': 'License Document',
            'type': 'Factory Type'
        }
        help_texts = {
            'factoryName': 'Enter the name of the factory.',
            'location': 'Enter the location of the factory.',
            'owner': 'Enter the owner\'s name.',
            'contact': 'Enter a valid contact number.',
            'email': 'Enter a valid email address.',
            'license': 'Upload the factory license document.',
            'type': 'Select the type of factory.'
        }
