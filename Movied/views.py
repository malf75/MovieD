from django.shortcuts import render, redirect, get_object_or_404
from Movied.models import Postagem, Profile
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.utils import timezone

def index(request):
    postagens = Postagem.objects.all().order_by("-data_postagem")
    
    if request.method == "POST" and request.user.is_authenticated:

        postagem_text = request.POST.get('postagemt', None)
        user = request.user
        postagem = Postagem.objects.create(
            user=user,
            comentario=postagem_text,
            data_postagem=timezone.now()
        )

        postagem.save()
        return redirect('index')
    
    if request.method == "POST" and not request.user.is_authenticated:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')
        

    return render(request, 'movied/index.html', {'posts': postagens})

def login(request):

    context = {}

    if request.method == "POST":

        erros = {}

        nome = request.POST.get('username', None)
        password = request.POST.get('password', None)

        usuario = auth.authenticate(
            request,
            username=nome,
            password=password
        )

        if usuario:
            auth.login(request, usuario)
            return redirect('index')
        else:
            erros['login'] = "Account Not Found"
        
        if erros:
            context['erros'] = erros

    return render(request, 'movied/login.html', context=context)

def signup(request):

    context = {}

    if request.method == "POST":

        erros = {}

        nome = request.POST.get('nome', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if password != password2:
            erros['password'] = "Passwords Are Different"
        
        if ' ' in password:
            erros['password'] = "Spaces Are Not Permited"

        if User.objects.filter(username=nome).exists():
            erros['username'] = "Username Already Exists"
        
        if ' ' in nome:
            erros['username'] = "Spaces Are Not Permited"
        
        if User.objects.filter(email=email).exists():
            erros['email'] = "Email Already Registered"

        if erros:
            context['erros'] = erros

        else:
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=password
            )
            usuario.save()
            return redirect('login')

    return render(request, 'movied/signup.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect('index')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        postagens = Postagem.objects.filter(user_id=pk).order_by("-data_postagem")

        if request.method == "POST":
            if 'follow' in request.POST:
                current_user_profile = request.user.profile
                action = request.POST.get('follow')
                action2 = request.POST.get('mudar-foto')
                if action == "unfollow":
                    current_user_profile.follows.remove(profile)
                elif action == "follow":
                    current_user_profile.follows.add(profile)

                if action2 == "mudar-foto":
                    new_image = request.FILES.get('nova-imagem')
                    if new_image:
                        current_user_profile.profile_image = new_image
                        current_user_profile.save()

                current_user_profile.save()

        return render(request, "movied/profile.html", {"profile":profile, "posts":postagens})
    else:
        return redirect('index')
    
def postagem_like(request, pk):
    if request.user.is_authenticated:
        postagem = get_object_or_404(Postagem, id=pk)
        if postagem.likes.filter(id=request.user.id):
            postagem.likes.remove(request.user)
        else:
            postagem.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')
    
