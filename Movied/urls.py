from django.urls import path
from Movied import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/following/<int:pk>', views.following, name='following'),
    path('postagem_like/<int:pk>', views.postagem_like, name='postagem_like'),
    path('postagem_comentarios/<int:pk>', views.comentarios, name='comentarios'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('profile/edit/<int:pk>', views.profile_edit, name='profileedit'),
    path('deletar_postagem/<int:pk>', views.deletar_postagem, name='deletar_postagem'),
    path('reportar_postagem/<int:pk>', views.reportar_postagem, name='reportar_postagem'),
    path('deletar_comentario/<int:pk>', views.deletar_comentario, name='deletar_comentario'),
    path('reportar_comentario/<int:pk>', views.reportar_comentario, name='reportar_comentario'),
    path('search', views.search, name='search'),
]