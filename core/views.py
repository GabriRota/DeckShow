from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from django_countries import countries


def index(request):
    user_profile = None
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()

    titolo = request.POST.get('titolo', '').strip()
    utente = request.POST.get('proprietario', '').strip()
    condizioni = request.POST.get('condizioni', '')
    ordinamento = request.POST.get('ordinamento', 'data_desc')

    if titolo: 
        posts = posts.filter(title__icontains = titolo)
    if utente:
        posts = posts.filter(user__icontains = utente)
    if condizioni:
        posts = posts.filter(conditions = condizioni)

    if ordinamento == 'data_asc':
        posts = posts.order_by('date_time')
    elif ordinamento == 'data_desc':
        posts = posts.order_by('-date_time')
    elif ordinamento == 'like_desc':
        posts = posts.order_by('-n_of_like')
    elif ordinamento == 'wishlist_desc':
        posts = posts.order_by('-n_of_wishlist')

    contenuto = {
        'user_profile': user_profile,
        'posts' : posts,
        'filter' : {
            'titolo' : titolo,
            'proprietario': utente,
            'condizioni': condizioni,
            'ordinamento' : ordinamento
        }
    }
    return render(request, 'index.html', contenuto)

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
                #una volta creato l'account, l'utente viene reindirizzato nella pagina per modificare il profilo
                user_login = auth.authenticate(username = username, password = password)
                auth.login(request, user_login)

                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Le password non coincidono')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user.username).order_by('-date_time')
    return render(request, 'profile.html',
                  {'user': user, 'user_profile': user_profile, 'posts':posts,})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def perTe(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'perTe.html', {'user_profile': user_profile})

@login_required(login_url='login')
def settings(request):
    user_object = request.user
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        user_profile.name = request.POST.get('name', user_profile.name)
        user_profile.surname = request.POST.get('surname', user_profile.surname)
        user_profile.nationality = request.POST.get('nationality', user_profile.nationality)

        if 'img_profilo' in request.FILES:
            user_profile.img_profilo = request.FILES['img_profilo']
        
        user_profile.save()
        return redirect('user_profile', user_id=request.user.id)
    return render(request, 'settings.html', {
        'user_profile': user_profile,
        'countries': list(countries)
    })

@login_required(login_url='login')
def create(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        user = request.user.username
        title = request.POST['title']
        image_front = request.FILES.get('img_front')
        image_back =  request.FILES.get('img_back')
        description = request.POST.get('description', '').strip() or ''
        conditions = request.POST['conditions']
        link = request.POST.get('link', '').strip() or ''

        new_post = Post.objects.create(user=user, image_front=image_front, title=title, image_back=image_back, description=description, conditions=conditions, link=link)
        new_post.save()

        return redirect('user_profile', user_id=user_object.id)
    else:
        return render(request, 'create.html', {'user_profile': user_profile})

@login_required(login_url='login')   
def edit_post(request, post_id):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user.username:
        return redirect('index')
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')
        post.conditions = request.POST.get('conditions')
        post.link = request.POST.get('link', '')
    
        if 'image_front' in request.FILES:
            post.image_front = request.FILES['image_front']
        if 'image_back' in request.FILES:
            post.image_back = request.FILES['image_back']

        post.save()
        return redirect('user_profile', user_id=user_object.id)

    return render(request, 'edit.html', {'post': post, 'user_profile' : user_profile} )

@login_required(login_url='login')
def delete_post(request, post_id):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user.username:
        return redirect('index')
    
    post.delete()
    return redirect ('user_profile', user_id=user_object.id)