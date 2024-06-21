from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required #Added import here
from .forms import UserProfileForm
from myapp.models import Order

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required # Added decorator here
def profile(request): 
    orders = Order.objects.filter(customer_id=request.user.id,completed=True)
    return render(request, 'users/profile.html',{'orders':orders})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Assuming you have a profile view to redirect to
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/update_profile.html', {'form': form})

