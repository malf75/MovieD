from django.contrib import admin
from Movied.models import Postagem
from django.contrib.auth.models import User, Group
from .models import Profile

admin.site.unregister(Group)

class ListandoPostagens(admin.ModelAdmin):
    list_display = ("id", "comentario", "data_postagem")
    list_display_links = ("id", "comentario")
    search_fields = ("comentario", "id")
    list_per_page = 10

class ProfileInLine(admin.StackedInline):
    model=Profile

class UserAdmin(admin.ModelAdmin):
    model=User
    inlines= [ProfileInLine]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Postagem, ListandoPostagens)


