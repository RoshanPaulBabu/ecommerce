from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Customer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from .forms import CustomerUpdateForm


# Create your views here.
# Create your views here.
def index(request):
    return render(request, 'index.html')



def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')  # Corrected variable name
        last_name = request.POST.get('last_name')  # Corrected variable name
        email = request.POST.get('email')  # Corrected variable name
        phone_no = request.POST.get('phone_no')  # Corrected variable name
        password = request.POST.get('password')  # Corrected variable name
        confirm_password = request.POST.get('confirm_password')  # Corrected variable name

        if password != confirm_password:
            messages.error(request, 'Passwords Do Not Match!')
            return render(request, 'customer/register.html')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, '\n' + '\n'.join(e.messages))
            return render(request, 'customer/register.html')

        try:
            # Creating a User object
            user = User.objects.create_user(username=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            password=password)

            # Creating a Customer object (assuming you have a Customer model)
            customer = Customer.objects.create(first_name=first_name,
                                               last_name=last_name,
                                               email=email,
                                               phone_no=phone_no)

            # Authenticating the user
            user = authenticate(username=email, password=password)
            login(request, user)

            messages.success(request, 'Your Account Has Been Registered Successfully!')
            return redirect('index')
        except Exception as e:
            messages.error(request, 'Account Was Not Created! Try Again')
            return render(request, 'customer/register.html')

    return render(request, 'customer/register.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('index')  # Change 'index' to your desired redirect URL after login
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return render(request, 'customer/login.html')  # Change 'login.html' to your login template path
    return render(request, 'customer/login.html')  # Change 'login.html' to your login template path

def user_logout(request):
    logout(request)
    return redirect('index') 

from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from .models import Customer

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = request.user  # Assuming the user is already logged in

        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully.")
                return redirect('login')
            else:
                messages.error(request, "New passwords do not match.")
        else:
            messages.error(request, "Old password is incorrect.")

    return render(request, 'customer/change_password.html')

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + user.password + str(timestamp)
        )

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = CustomTokenGenerator().make_token(user)
            reset_password_url = request.build_absolute_uri('/reset_password/{}/{}/'.format(uid, token))
            email_subject = 'Reset Your Password'
            email_body = render_to_string('customer/reset_password_email.html', {
                'reset_password_url': reset_password_url,
                'user': user,
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
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
    return render(request, 'customer/forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and CustomTokenGenerator().check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully. You can now login with your new password.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, 'customer/reset_password.html')
    else:
        messages.error(request, "Invalid reset link. Please try again or request a new reset link.")
        return redirect('login')


@login_required
def update_personal_info(request):
    user = request.user
    try:
        customer = user.customer  # Retrieve the associated Customer object
    except Customer.DoesNotExist:
        # If Customer object doesn't exist, create one
        customer = Customer(user=user)
        customer.save()

    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful update
    else:
        # Populate initial values from the existing Customer object
        form = CustomerUpdateForm(instance=customer, initial={
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone_no': customer.phone_no,
        })
    return render(request, 'customer/update_personal_info.html', {'form': form})