from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

NOTIFICATION_CHOICES = {
     "LK":"Like",
     "FL":"Follow",
     "CM":"Comment",
}

    
class Filmes(models.Model):
    Poster_Link = models.URLField(null=True, blank=True)
    Series_Title = models.CharField(null=False, blank=False, max_length=110)
    Released_Year = models.IntegerField(null=True, blank=True)
    Runtime = models.CharField(null=False, blank=False, max_length=10)
    Genre = models.CharField(null=False, blank=False, max_length=50)
    Rating = models.FloatField(null=False, blank=False)
    Overview = models.TextField(null=False, blank=False, max_length=400)
    Streaming = models.URLField(null=True, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
         return(
              f"{self.Series_Title} "
              f"{self.Released_Year}"
         )
    
class Postagem(models.Model):
    comentario = models.TextField(null=False, blank=False, max_length=400)
    data_postagem = models.DateTimeField(default=datetime.now, blank=False)
    user = models.ForeignKey(User, related_name='comentarios', on_delete=models.DO_NOTHING, default=None)
    likes = models.ManyToManyField(User, related_name="postagem_like", blank=True)
    reported = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)
    filmes = models.ManyToManyField(Filmes, related_name='postagens', blank=True)

    def number_of_likes(self):
         return self.likes.count()

    def __str__(self):
         return(
              f"{self.user} "
              f"({self.data_postagem})"
         )
    
class Comentarios(models.Model):
    id = models.AutoField(primary_key=True)
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
    
def user_directory_path(instance, filename):
    return 'media/images/{0}/{1}'.format(instance.user.username, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    bio = models.TextField(null=True, blank=True, max_length = 80)
    
    def __str__(self):
        return (f"{self.user.username}"
            )
    
class Notification(models.Model):
     user = models.ForeignKey(User, related_name='Notifications_user', on_delete=models.CASCADE)
     notificacao = models.CharField(null=True, blank=True, max_length = 200)
     notification_sender = models.ForeignKey(User, related_name='Notification_sender', on_delete=models.CASCADE, default=None)
     type = models.CharField(max_length=20, choices=NOTIFICATION_CHOICES, default='Like')

     def __str__(self):
          return self.notificacao

    
class Suggestions(models.Model):
    user = models.ForeignKey(User, related_name='suggestions', on_delete=models.DO_NOTHING, default=None)
    Series_Title = models.CharField(null=False, blank=False, max_length=120)
    Released_Year = models.IntegerField(null=False, blank=False)
    Runtime = models.CharField(null=False, blank=False, max_length=10)
    Genre = models.CharField(null=False, blank=False, max_length=50)
    Rating = models.FloatField(null=False, blank=False)
    Overview = models.TextField(null=False, blank=False, max_length=400)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return (f"{self.Series_Title}"
            )
    
class List(models.Model):
     user = models.ForeignKey(User, related_name='List_user', on_delete=models.CASCADE)
     filmes = models.ManyToManyField(Filmes, related_name='lists', blank=True)

     def __str__(self):
          return self.filmes


def create_profile(sender, instance, created, **kwargs):
    if created:
            user_profile = Profile(user=instance)
            user_profile.save()

post_save.connect(create_profile, sender=User)

@receiver(m2m_changed, sender=Profile.follows.through)
def followed(sender, instance, action, reverse, model, pk_set, **kwargs):
     if action == 'post_add' and not reverse:
          user = model.objects.get(pk=pk_set.pop()).user
          notification_sender = instance.user
          message = f"{notification_sender} started following you"
          if Notification.objects.filter(user=user, notificacao=message, notification_sender=notification_sender, type='FL').exists():
               pass
          else:
               notification = Notification.objects.create(user=user, notificacao=message, notification_sender=notification_sender, type='FL')
               notification.save()
          