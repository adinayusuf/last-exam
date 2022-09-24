from django.contrib import admin
from webapp.models import *

admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(FavoritePhoto)
admin.site.register(FavoriteAlbum)
