from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomerRegistrationForm, LoginForm
from .models import Customer
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(email=email, password=password)
            return redirect('index') 
        except Customer.DoesNotExist:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'customer/login.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth import hashers
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        customer = request.user  # Assuming the user is already logged in

        # Check if the old password matches the current password of the user
        if customer.check_password(old_password):
            if new_password == confirm_password:
                # Hash the new password before saving it
                customer.set_password(new_password)
                customer.save()
                messages.success(request, "Password changed successfully.")
                return redirect('login')
            else:
                messages.error(request, "New passwords do not match.")
        else:
            messages.error(request, "Old password is incorrect.")

    return render(request, 'customer/change_password.html')


class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, customer, timestamp):
        return (
            str(customer.pk) + customer.password + str(timestamp)
        )

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            customer = Customer.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(customer.pk))
            token = CustomTokenGenerator().make_token(customer)
            reset_password_url = request.build_absolute_uri('/reset_password/{}/{}/'.format(uid, token))
            email_subject = 'Reset Your Password'
            email_body = render_to_string('customer/reset_password_email.html', {
                'reset_password_url': reset_password_url,
                'customer': customer,
            })
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.send(fail_silently=False)
            messages.success(request, 'An email has been sent to your email address with instructions on how to reset your password.')
            return redirect('login')
        except Customer.DoesNotExist:
            messages.error(request, "Customer with this email does not exist.")
    return render(request, 'customer/forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        customer = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        customer = None

    if customer is not None and CustomTokenGenerator().check_token(customer, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                # Hash the password before assigning it to the customer object
                customer.password = new_password
                customer.save()
                messages.success(request, "Password reset successfully. You can now login with your new password.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, 'customer/reset_password.html')
    else:
        messages.error(request, "Invalid reset link. Please try again or request a new reset link.")
        return redirect('login')