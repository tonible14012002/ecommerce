import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render

from account.decorator import ajax_required
from .models import CustomerInfo
from .form import RegistrationForm, CustomerInfoForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import password_reset_token, account_activation_token

from django.views.decorators.http import require_http_methods

from account import form
# Create your views here.

User = get_user_model()

def login_page(request):
    if request.user.is_authenticated:
        return redirect('store:products_list')
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form })

@ajax_required
@require_http_methods(['POST'])
def login_user(request):
    user_info = json.loads(request.body)
    user = authenticate(username=user_info['username'],
                        password=user_info['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status':'ok'})
    # get inactive user
    try:
        user = User.objects.get(username=user_info['username'])
    except User.DoesNotExist:
        user = None
    if user is not None and not user.is_active:
        return JsonResponse({'status':'inactive'})
    else:
        return JsonResponse({'status':'error'})
    

@login_required
def password_change_form(request):
    form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})

@login_required
@ajax_required
@require_http_methods(['POST'])
def password_change_request(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'error', 'errors':form.errors})

def password_reset_form(request):
    if request.user.is_authenticated:
        return redirect('store:products_list')
    form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})

@ajax_required
@require_http_methods(['POST'])
def password_reset_request(request):
    email = request.POST.get('email')
    try:
        user = User.objects.get(email=email)
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return JsonResponse({'status': 'error'})
    site = get_current_site(request)
    html_message = render_to_string('registration/password_reset_email.html',
                                    context={
                                        'domain': site.domain,
                                        'protocol': 'http',
                                        'user': user,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token' : password_reset_token.make_token(user)
                                    })
    plain_message = strip_tags(html_message)
    # send_mail(
    #     'PASSWORD RESET REQUEST',
    #     plain_message,
    #     settings.EMAIL_HOST_USER,
    #     (user,),
    #     html_message=html_message
    # )
    print(plain_message)
    return JsonResponse({'status':'ok'})

def password_reset_confirm_form(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, OverflowError, ValueError, User.DoesNotExist) :
        user = None
    if user and password_reset_token.check_token(user, token):
        form = SetPasswordForm(user=user)
        context = {
            'form' :form,
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'registration/password_reset_confirm.html', context)
    return render(request, 'registration/expired_page.html')

@ajax_required
@require_http_methods(['POST'])
def password_reset_confirm_request(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, OverflowError, ValueError, User.DoesNotExist) :
        user = None
    if user and password_reset_token.check_token(user, token):
        form = SetPasswordForm(user=user,data=request.POST)
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

def register_page(request):
    form = RegistrationForm()
    return render(request, 'registration/register.html', {'form':form})

@ajax_required
@require_http_methods(['POST'])
def register_request(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data['password'])
        user.save()
        site = get_current_site(request)
        html_message = render_to_string('registration/activate_account_email.html',
                                        context={
                                            'domain': site.domain,
                                            'protocol': 'http',
                                            'user': user,
                                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token' : account_activation_token.make_token(user)
                                        })
        plain_message = strip_tags(html_message)
        # send_mail(
        #     'PASSWORD RESET REQUEST',
        #     plain_message,
        #     settings.EMAIL_HOST_USER,
        #     (user,),
        #     html_message=html_message
        # )
        print(plain_message)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status':'error', 'errors': form.errors})
    
def account_activation(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=uid)
    except (ValueError, TypeError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activation_success.html', {'user': user})
    return render(request, 'registration/expired_page.html')

@ajax_required
@require_http_methods(['POST'])
def account_activation_request(request):
    user_info = json.loads(request.body)
    print(user_info)
    try:
        user = User.objects.get(username=user_info['username'])
    except User.DoesNotExist:
        user = None
    if user is not None:
        site = get_current_site(request)
        html_message = render_to_string('registration/activate_account_email.html',
                                        context={
                                            'domain': site.domain,
                                            'protocol': 'http',
                                            'user': user,
                                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token' : account_activation_token.make_token(user)
                                        })
        plain_message = strip_tags(html_message)
        # send_mail(
        #     'PASSWORD RESET REQUEST',
        #     plain_message,
        #     settings.EMAIL_HOST_USER,
        #     (user,),
        #     html_message=html_message
        # )
        print(plain_message)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status':'error'})