from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Postagem(models.Model):
    comentario = models.TextField(null=False, blank=False, max_length=400)
    data_postagem = models.DateTimeField(default=datetime.now, blank=False)
    user = models.ForeignKey(User, related_name='comentarios', on_delete=models.DO_NOTHING, default=None)
    likes = models.ManyToManyField(User, related_name="postagem_like", blank=True)
    reported = models.BooleanField(default=False)

    def number_of_likes(self):
         return self.likes.count()

    def __str__(self):
         return(
              f"{self.user} "
              f"({self.data_postagem})"
         )
    
class Comentarios(models.Model):
    comentario = models.TextField(null=True, blank=True, max_length=400)
    data_comentario = models.DateTimeField(default=datetime.now, blank=False)
    user = models.ForeignKey(User, related_name='comentarios_postagem_user', on_delete=models.DO_NOTHING, default=None)
    postagem = models.ForeignKey(Postagem, related_name='comentarios_postagem', default=None, on_delete=models.CASCADE)
    reported = models.BooleanField(default=False)

    def __str__(self):
         return(
              f"{self.comentario}"
              f"{self.data_comentario}"
         )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    bio = models.TextField(null=True, blank=True, max_length = 80)
    
    def __str__(self):
        return (f"{self.user.username}"
                f"({self.user.id})"
            )
    
class Suggestions(models.Model):
    user = models.ForeignKey(User, related_name='suggestions', on_delete=models.DO_NOTHING, default=None)
    Series_Title = models.CharField(null=False, blank=False, max_length=50)
    Released_Year = models.IntegerField(null=False, blank=False)
    Runtime = models.CharField(null=False, blank=False, max_length=10)
    Genre = models.CharField(null=False, blank=False, max_length=50)
    Rating = models.FloatField(null=False, blank=False)
    Overview = models.TextField(null=False, blank=False, max_length=400)

    def __str__(self):
        return (f"{self.Series_Title}"
            )

def create_profile(sender, instance, created, **kwargs):
    if created:
            user_profile = Profile(user=instance)
            user_profile.save()

post_save.connect(create_profile, sender=User)