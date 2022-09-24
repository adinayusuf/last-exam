from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Album(models.Model):
    description = models.CharField(max_length=2000, verbose_name='Название')
    title = models.CharField(max_length=50, verbose_name='Текст')
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False, blank=True, verbose_name='Приватный')

    def __str__(self):
        return self.title


class Photo(models.Model):
    image = models.FileField(verbose_name='Изображение', upload_to='images')
    description = models.CharField(max_length=50, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', on_delete=models.CASCADE, related_name='photos')
    album = models.ForeignKey('webapp.Album', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Альбом')
    is_private = models.BooleanField(default=False, blank=True, verbose_name='Приватный')

    def __str__(self):
        return self.description


class FavoritePhoto(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='fav_photos', on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, related_name='fav_users', on_delete=models.CASCADE)


class FavoriteAlbum(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='fav_albums', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='fav_users', on_delete=models.CASCADE)
