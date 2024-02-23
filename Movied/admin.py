from django.contrib import admin
from Movied.models import Postagem, Suggestions, Comentarios, Filmes, Notifications
from django.contrib.auth.models import User, Group
from .models import Profile

admin.site.unregister(Group)

class ListandoPostagens(admin.ModelAdmin):
    list_display = ("id", "comentario", "data_postagem")
    list_display_links = ("id", "comentario")
    search_fields = ("comentario", "id")
    list_filter = ('reported',)
    list_per_page = 10

class ListandoComentarios(admin.ModelAdmin):
    list_display = ("id", "comentario", "data_comentario")
    list_display_links = ("id", "comentario")
    search_fields = ("comentario", "id")
    list_per_page = 10
    list_filter = ('reported',)

class ProfileInLine(admin.StackedInline):
    model=Profile

class ListSuggestions(admin.ModelAdmin):
    list_display = ("id", "Series_Title")
    list_display_links = ("id", "Series_Title")
    search_fields = ("id", "Series_Title")
    list_per_page = 10

class ListFilmes(admin.ModelAdmin):
    list_display = ("id", "Series_Title")
    list_display_links = ("id", "Series_Title")
    search_fields = ("id", "Series_Title")
    list_per_page = 500    
    list_filter = ('Genre',)

class ListNotifications(admin.ModelAdmin):
    list_display = ("id", "notificacao")
    list_display_links = ("id", "notificacao")
    list_per_page = 10


class UserAdmin(admin.ModelAdmin):
    model=User
    inlines= [ProfileInLine]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Postagem, ListandoPostagens)

admin.site.register(Comentarios, ListandoComentarios)

admin.site.register(Suggestions, ListSuggestions)

admin.site.register(Filmes, ListFilmes)

admin.site.register(Notifications, ListNotifications)



