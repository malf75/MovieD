from django.shortcuts import render, redirect, get_object_or_404
from Movied.models import Postagem, Profile, Suggestions, Comentarios, Filmes, Notification
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from django.core.files.storage import default_storage
import re

def get_filme_info(request):
    if request.user.is_authenticated:
        filmes = Filmes.objects.all()
        filme_info = {
            "filmes": []
        }
        for filme in filmes:
            filme_info["filmes"].append({
                "Series_Title": filme.Series_Title,
            })

        return JsonResponse(filme_info, safe=False)

def index(request):
    if request.user.is_authenticated:
        postagens = Postagem.objects.all().order_by("-data_postagem")
        include_follows = request.GET.get('include_follows')
        followed_profiles = request.user.profile.follows.all()
        if include_follows == 'on':
            related_postagens = Postagem.objects.filter(user__profile__in=followed_profiles)
            top_posts = Filmes.objects.filter(postagens__in=related_postagens).annotate(total_citations=Count('postagens')).filter(total_citations__gt=0).order_by('-total_citations')[:3]
        else:
            top_posts = Filmes.objects.annotate(total_citations=Count('postagens')).filter(total_citations__gt=0).order_by('-total_citations')[:3]
    
        if request.method == "POST":

            postagem_text = request.POST.get('postagemt', None)
            user = request.user
            titulo = Filmes.objects.values_list('Series_Title', flat=True)
            pattern = r'\b(?!:.)\s*(?:' + '|'.join(map(re.escape, titulo)) + r')\b(?!:.)\s*'
            pattern_pink = r'Pink Floyd: The Wall'
            pink_match = re.search(pattern_pink, postagem_text)

            if pink_match: 
                titulo_matched = pink_match.group()
                filme = Filmes.objects.filter(Series_Title__iexact=titulo_matched.strip()).first()
                if filme:
                    postagem = Postagem.objects.create(
                        user=user,
                        comentario=postagem_text,
                        data_postagem=timezone.now(),
                    )
                    postagem.filmes.set([filme])
                    postagem.save()

                    return redirect('index')
                
            else:
                filme_match = re.search(pattern, postagem_text)
                if filme_match:
                    titulo_matched = filme_match.group()
                    filme = Filmes.objects.filter(Series_Title__iexact=titulo_matched.strip()).first()
                    if filme:
                        postagem = Postagem.objects.create(
                            user=user,
                            comentario=postagem_text,
                            data_postagem=timezone.now(),
                        )
                        postagem.filmes.set([filme])
                        postagem.save()
                else:
                    filme = None
                    postagem = Postagem.objects.create(
                        user=user,
                        comentario=postagem_text,
                        data_postagem=timezone.now(),
                    )
                    postagem.save()

                return redirect('index')
        
    else:
        return redirect('login')

    return render(request, 'movied/index.html', {'posts': postagens, 'top_posts':top_posts})

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
    return redirect('login')

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
            notification = Notification.objects.filter(user=postagem.user, notificacao=f'{request.user} liked your review of {"".join([filme.Series_Title for filme in postagem.filmes.all()])}', notification_sender=request.user)
            if notification.exists():
                pass
            else:
                notification = Notification.objects.create(
                user=postagem.user,
                notificacao=f'{request.user} liked your review of {"".join([filme.Series_Title for filme in postagem.filmes.all()])}',
                notification_sender=request.user
                )
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
            comentario = Comentarios.objects.filter(comentario=comentario_texto, postagem=postagem, user=request.user)
            if comentario.exists():
                messages.warning(request, ('You Have Already Commented This'))
            else:
                Comentarios.objects.create(comentario=comentario_texto, postagem=postagem, user=request.user)
                notification = Notification.objects.create(
                user=postagem.user,
                notificacao=f'{request.user} commented your review of {"".join([filme.Series_Title for filme in postagem.filmes.all()])}',
                notification_sender=request.user,
                type="CM"
                )
                if notification.user == notification.notification_sender:
                    pass
                else:
                    notification.save()
                return redirect('comentarios', pk=pk)
            
        return render(request, 'movied/comentarios.html', {'postagem':postagem})
    
def deletar_postagem(request, pk):
    if request.user.is_authenticated:
        postagem = get_object_or_404(Postagem, id=pk)
        if request.user.username == postagem.user.username:
            postagem.delete()
            return redirect('index')
    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('login')
    
def deletar_comentario(request, pk):
    if request.user.is_authenticated:
        comentario = get_object_or_404(Comentarios, id=pk)
        if request.user.username == comentario.user.username:
            comentario.delete()
            return redirect('index')
    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('login')
    
def reportar_postagem(request, pk):
    if request.user.is_authenticated:
        postagem = get_object_or_404(Postagem, id=pk)
        postagem.reported = True
        postagem.save()
        return redirect('index')
    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('login')
    
def reportar_comentario(request, pk):
    if request.user.is_authenticated:
        comentario = get_object_or_404(Comentarios, id=pk)
        comentario.reported = True
        comentario.save()
        return redirect('index')
    else:
        messages.warning(request, ('You Must Be Logged In'))
        return redirect('login')
    
def search(request):
    query = request.POST.get('query')
    posts = Postagem.objects.filter(comentario__icontains=query)
    users = User.objects.filter(username__icontains=query)
    return render(request, 'movied/search.html', {'posts':posts, 'query':query, 'users':users})

def preferences(request):
    if request.user.is_authenticated:

        return render(request, 'movied/preferences.html')

def notifications(request, pk):
    if request.user.is_authenticated and pk == request.user.id:
        notification = Notification.objects.filter(user_id=pk).order_by("-id")
        
        return render(request, 'movied/notifications.html', {'notification':notification})