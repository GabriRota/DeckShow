from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

def index(request):
    user_profile = None
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    return render(request, 'index.html', {'user_profile': user_profile})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Le credenziali non sono corrette')
            return redirect('login')
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if password == confirmPassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email già usata')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username già usato')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #voglio che venga creato anche un profilo quando viene fatto l'account
                #una volta creato l'account, l'utente viene reindirizzato nella pagina per modificare il profilo
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('login')

        else:
            messages.info(request, 'Le password non coincidono')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = Profile.objects.get(user=user)
    return render(request, 'profile.html', {'user': user, 'user_profile': user_profile})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def perTe(request):
    user_profile = None
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    return render(request, 'perTe.html', {'user_profile': user_profile})

