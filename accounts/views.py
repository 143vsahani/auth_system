from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log the user in
            return redirect('login_view')  # Redirect to the login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('upload_video')  # Redirect to the 'upload_video' page after login
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    
    return render(request, 'accounts/login.html')
@login_required
def home(request):
    return render(request, 'accounts/home.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login_view')  # Redirect to the login page after logout
