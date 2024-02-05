from django.urls import path
from Movied import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('postagem_like/<int:pk>', views.postagem_like, name='postagem_like'),
    path('suggestions/', views.suggestions, name='suggestions'),
]