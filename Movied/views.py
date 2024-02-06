from django.shortcuts import render, redirect, get_object_or_404
from Movied.models import Postagem, Profile, Suggestions, Comentarios
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.utils import timezone
from django.http import JsonResponse


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
                if action == "unfollow":
                    current_user_profile.follows.remove(profile)
                elif action == "follow":
                    current_user_profile.follows.add(profile)

                current_user_profile.save()

        return render(request, "movied/profile.html", {"profile":profile, "posts":postagens})
    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')
    
def followers(request,pk):
    if request.user.is_authenticated:
        profiles = Profile.objects.get(user_id=pk)
    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')

    return render(request, 'movied/followers.html', {"profiles":profiles})

def following(request,pk):
    if request.user.is_authenticated:
        profiles = Profile.objects.get(user_id=pk)
    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')

    return render(request, 'movied/following.html', {"profiles":profiles})
    
def postagem_like(request, pk):
    if request.user.is_authenticated:
        postagem = get_object_or_404(Postagem, id=pk)
        if postagem.likes.filter(id=request.user.id):
            postagem.likes.remove(request.user)
        else:
            postagem.likes.add(request.user)

        data = {
            'likes_count': postagem.likes.count(),
            'user_liked': postagem.likes.filter(id=request.user.id).exists()
        }
        return JsonResponse(data)

    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')
    
def suggestions(request):

    if request.method == "POST" and request.user.is_authenticated:

        nome = request.POST.get('nome-filme', None)
        ano = request.POST.get('ano-filme', None)
        duracao = request.POST.get('duracao-filme', None)
        genero = request.POST.get('genero-filme', None)
        rating = request.POST.get('rating-filme', None)
        sinopse = request.POST.get('sinopse-filme', None)
        user = request.user
        sugestao = Suggestions.objects.create(
            user=user,
            Series_Title=nome,
            Released_Year=ano,
            Runtime=duracao,
            Genre=genero,
            Rating=rating,
            Overview=sinopse,
        )

        sugestao.save()
        return redirect('index')
    
    if not request.user.is_authenticated:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')

    return render(request, 'movied/suggestions.html')
    
def profile_edit(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            current_user = request.user
            profile = get_object_or_404(Profile, user=current_user)
            erros = {}

            nome = request.POST.get('nome', None)
            bio = request.POST.get('bio', None)
            imagem = request.FILES.get('profile_picture')

            if nome:
                if User.objects.filter(username=nome).exclude(pk=current_user.pk).exists():
                    erros['username'] = "Username Already Exists"
                if ' ' in nome:
                    erros['username'] = "Spaces Are Not Permitted"

            else:
                nome = current_user.username
            
            if bio:
                profile.bio = bio

            if imagem:
                profile.profile_image = imagem

            if erros:
                context = {'erros': erros, 'profiles': profile}
                return render(request, 'movied/profileedit.html', context)
            else:
                if nome != current_user.username:
                    current_user.username = nome
                    current_user.save()
                profile.save()
                return redirect('profile', pk=pk)
        else:
            profiles = Profile.objects.get(user__id=request.user.id)
            return render(request, 'movied/profileedit.html', {"profiles": profiles})
    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')
    
def comentarios(request, pk):
    if request.user.is_authenticated:
        postagem = get_object_or_404(Postagem, id=pk)
        if request.method == 'POST':
            comentario_texto = request.POST.get('comentario')
            Comentarios.objects.create(comentario=comentario_texto, postagem=postagem, user=request.user)
            return redirect('comentarios', pk=pk)
        return render(request, 'movied/comentarios.html', {'postagem':postagem})
    
def comentario_like(request, pk):
    if request.user.is_authenticated:
        comentario = get_object_or_404(Comentarios, id=pk)
        if comentario.likes.filter(id=request.user.id):
            comentario.likes.remove(request.user)
        else:
            comentario.likes.add(request.user)

        data = {
            'likes_count': comentario.likes.count(),
            'user_liked': comentario.likes.filter(id=request.user.id).exists()
        }
        return JsonResponse(data)

    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('index')