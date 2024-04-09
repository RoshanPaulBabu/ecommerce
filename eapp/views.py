from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Customer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from .models import Customer


# Create your views here.
# Create your views here.
def index(request):
    return render(request, 'index.html')



def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full-name')
        email = request.POST.get('your-email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        phone_number = request.POST.get('phone-number')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords Do Not Match!')
            return render(request, 'customer/register.html')

        # Check password strength using Django's built-in validators
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return render(request, 'customer/register.html')

        # Create user
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
        except:
            messages.error(request, 'Email already exists!')
            return render(request, 'customer/register.html')

        # Create customer
        customer = Customer.objects.create(user=user, customer_name=full_name, email=email, contact_number=phone_number)
        
        # Authenticate and login user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Your Account Has Been Registered Successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Failed to login user.')
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

            # Render both HTML and plain text versions of the email
            email_body_html = render_to_string('customer/reset_password_email.html', {
                'reset_password_url': reset_password_url,
                'user': user,
            })
            email_body_text = "Click the following link to reset your password: {}".format(reset_password_url)

            # Create an EmailMultiAlternatives object to send both HTML and plain text versions
            email = EmailMultiAlternatives(
                email_subject,
                email_body_text,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.attach_alternative(email_body_html, 'text/html')  # Attach HTML version
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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer

@login_required
def edit_customer(request):
    # Retrieve the current logged-in user
    current_user = request.user
    # Check if the current user has a corresponding Customer instance
    try:
        customer = Customer.objects.get(user=current_user)
    except Customer.DoesNotExist:
        # Handle the case where the logged-in user does not have a corresponding Customer instance
        return HttpResponse("You are not associated with any customer profile.")

    if request.method == 'POST':
        # Update customer details with the data from the form
        customer.customer_name = request.POST['full-name']
        customer.email = request.POST['your-email']
        customer.contact_number = request.POST['phone-number']
        customer.save()

        # Update associated user's email
        current_user.email = request.POST['your-email']
        current_user.username = request.POST['your-email']
        current_user.save()

        # Redirect to the customer detail page after editing
        return redirect('index')

    # If it's a GET request, display the edit form with existing customer details
    return render(request, 'customer/edit_customer.html', {'customer': customer})