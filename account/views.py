from django.shortcuts import redirect, render
from .models import CustomerInfo
from .form import RegistrationForm, CustomerInfoForm
from django.contrib.auth.decorators import login_required
# Create your views here.

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
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form':form})

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

        
    