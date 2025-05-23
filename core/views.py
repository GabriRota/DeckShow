from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from django_countries import countries


def index(request):
    logged_in_profile = None
    if request.user.is_authenticated:
        logged_in_profile = Profile.objects.get(user=request.user)

    posts = Post.objects.select_related('user', 'user__profile').all()

    titolo = request.POST.get('titolo', '').strip()
    utente = request.POST.get('proprietario', '').strip()
    condizioni = request.POST.get('condizioni', '')
    ordinamento = request.POST.get('ordinamento', 'data_desc')

    if titolo: 
        posts = posts.filter(title__icontains = titolo)
    if utente:
        posts = posts.filter(user__username__icontains=utente)
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
        'logged_in_profile': logged_in_profile,
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
    profile_owner = get_object_or_404(User, id=user_id)
    profile_owner_profile = Profile.objects.get(user=profile_owner)
    posts = Post.objects.filter(user=profile_owner).order_by('-date_time')

    logged_in_profile = None
    is_following = None

    if request.user.is_authenticated:
        logged_in_profile = Profile.objects.get(user=request.user)
        is_following = profile_owner_profile in logged_in_profile.seguiti.all()

    return render(request, 'profile.html', {
        'user': profile_owner, 
        'profile_owner': profile_owner_profile, 
        'posts':posts, 
        'logged_in_profile': logged_in_profile,
        'is_following' : is_following,
        'n_followers' : profile_owner_profile.followers.count(),
        'n_seguiti' : profile_owner_profile.seguiti.count(),
        'followers' : profile_owner_profile.followers.all(),
        'seguiti' : profile_owner_profile.seguiti.all()
    })

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def perTe(request):
    logged_in_profile = Profile.objects.get(user=request.user)
    return render(request, 'perTe.html', {'logged_in_profile': logged_in_profile})

@login_required(login_url='login')
def settings(request):
    logged_in_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        logged_in_profile.name = request.POST.get('name', logged_in_profile.name)
        logged_in_profile.surname = request.POST.get('surname', logged_in_profile.surname)
        logged_in_profile.nationality = request.POST.get('nationality', logged_in_profile.nationality)

        if 'img_profilo' in request.FILES:
            logged_in_profile.img_profilo = request.FILES['img_profilo']
        
        logged_in_profile.save()
        return redirect('user_profile', user_id=request.user.id)
    return render(request, 'settings.html', {
        'logged_in_profile': logged_in_profile,
        'countries': list(countries)
    })

@login_required(login_url='login')
def create(request):
    logged_in_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        title = request.POST['title']
        image_front = request.FILES.get('img_front')
        image_back = request.FILES.get('img_back')
        description = request.POST.get('description', '').strip() or ''
        conditions = request.POST['conditions']
        link = request.POST.get('link', '').strip() or ''

        Post.objects.create(
            user=request.user,
            image_front=image_front,
            title=title,
            image_back=image_back,
            description=description,
            conditions=conditions,
            link=link
        )

        return redirect('user_profile', user_id=request.user.id)

    return render(request, 'create.html', {'logged_in_profile': logged_in_profile})

@login_required(login_url='login')   
def edit_post(request, post_id):
    logged_in_profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        messages.error(request, "Non sei autorizzato a modificare questo post.")
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
        return redirect('user_profile', user_id=request.user.id)

    return render(request, 'edit.html', {'post': post, 'logged_in_profile' : logged_in_profile} )


@login_required(login_url='login')
def delete_post(request, post_id):
    logged_in_profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        messages.error(request, "Non sei autorizzato ad eliminare questo post.")
        return redirect('index')
    
    post.delete()
    return redirect ('user_profile', user_id=request.user.id)

@login_required(login_url='login')
def follow_function(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_profile = target_user.profile
    logged_in_profile = request.user.profile

    if(target_profile == logged_in_profile):
        return HttpResponseForbidden("Operazione non consentita: non puoi seguire te stesso.")
    if target_profile in logged_in_profile.seguiti.all():
        logged_in_profile.seguiti.remove(target_profile)
    else:
        logged_in_profile.seguiti.add(target_profile)

    next = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    
    return redirect (next) #ritorna alla pagine dove è arrivata la richiesta

@login_required(login_url='login')
def like_function(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            liked = False
        else:
            post.liked_by.add(user)
            liked = True
        return JsonResponse({'liked': liked})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='login')
def wishlist_function(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.wishlisted_by.all():
            post.wishlisted_by.remove(user)
            in_wishlist = False
        else:
            post.wishlisted_by.add(user)
            in_wishlist = True
        return JsonResponse({'in_wishlist': in_wishlist})
    return JsonResponse({'error': 'Invalid request'}, status=400)

