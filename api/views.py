from webapp.models import Photo, FavoritePhoto, Album, FavoriteAlbum
from django.http import JsonResponse
from django.views import View


class FavoritePhotoApiView(View):
    def get(self, request, *args, **kwargs):
        object = Photo.objects.get(id=kwargs.get('pk'))
        photos = request.user.fav_photos.all().values_list('photo', flat=True)
        if object.id not in photos:
            FavoritePhoto.objects.create(user=request.user, photo=object)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class UnFavoritePhotoApiView(View):
    def get(self, request, *args, **kwargs):
        object = Photo.objects.get(id=kwargs.get('pk'))
        photos = request.user.fav_photos.all().values_list('photo', flat=True)
        if object.id in photos:
            FavoritePhoto.objects.get(user=request.user, photo=object).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class FavoriteAlbumView(View):
    def get(self, request, *args, **kwargs):
        object = Album.objects.get(id=kwargs.get('pk'))
        albums = request.user.fav_albums.all().values_list('album', flat=True)
        if object.id not in albums:
            FavoriteAlbum.objects.create(user=request.user, album=object)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class UnFavoriteAlbumApiView(View):
    def get(self, request, *args, **kwargs):
        object = Album.objects.get(id=kwargs.get('pk'))
        albums = request.user.fav_albums.all().values_list('album', flat=True)
        if object.id in albums:
            FavoriteAlbum.objects.get(user=request.user, album=object).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})
