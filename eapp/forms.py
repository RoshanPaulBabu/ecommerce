from django import forms
from .models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_no']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super(CustomerRegistrationForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if commit:
            user.set_password(password)
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_no']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
        }
