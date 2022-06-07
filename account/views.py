import imp
from multiprocessing import AuthenticationError
from multiprocessing.sharedctypes import Value
from operator import imod
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render

from account.decorator import ajax_required
from .models import CustomerInfo
from .form import RegistrationForm, CustomerInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import password_reset_token

from django.views.decorators.http import require_http_methods
# Create your views here.

User = get_user_model()

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('store:products_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form':form})

def password_change_form(request):
    form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})

@login_required
@ajax_required
@require_http_methods(['POST'])
def password_change(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid:
        form.save()
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'error', 'errors':form.error})

def password_reset_form(request):
    form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})

@ajax_required
@require_http_methods(['POST'])
def password_reset_request(request):
    email = request.POST.get('email')
    try:
        user = User.objects.get(emai=email)
    except User.DoesNotExist:
        return JsonResponse({'status': 'ok'})
    site = get_current_site(request)
    html_message = render_to_string('registration/password_reset_email.html',
                                    context={
                                        'domain': site.domain,
                                        'protocol': 'http',
                                        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token' : password_reset_token.make_token(user)
                                    })
    plain_message = strip_tags(html_message)
    send_mail(
        'PASSWORD RESET REQUEST',
        plain_message,
        settings.EMAIL_HOST_USER,
        (user,),
        html_message=html_message
    )
    return JsonResponse({'status':'ok'})

def password_reset_confirm_form(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, OverflowError, ValueError, User.DoesNotExist) :
        user = None
    if user and password_reset_token.check_token(user, token):
        form = SetPasswordForm()
        context = {
            'form' :form,
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'registration/password_reset_confirm.html', context)
    return render(request, 'registration/expired_page.html')

@ajax_required
@require_http_methods(['POST'])
def password_reset_confirm(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, OverflowError, ValueError, User.DoesNotExist) :
        user = None
    if user and password_reset_token.check_token(user, token):
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status': 'error', 'errors':form.errors})
    return JsonResponse({'status': 'expired'})

@login_required
def add_info(request):
    if request.method == 'POST':
        form = CustomerInfoForm(request.POST)
        if form.is_valid():
            customer_info = form.save(commit=False)
            customer_info.user = request.user
            customer_info.save()
            return redirect('store:products_list')
    else:
        form = CustomerInfoForm()
    return render(request, 'account/edit_info.html', {'form': form})

