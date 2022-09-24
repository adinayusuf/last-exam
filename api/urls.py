from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('photo/favorite/<int:pk>/', views.FavoritePhotoApiView.as_view(), name='fav_photo'),
    path('photo/unfavorite/<int:pk>/', views.UnFavoritePhotoApiView.as_view(), name='unfav_photo'),
    path('album/favorite/<int:pk>/', views.FavoriteAlbumView.as_view(), name='fav_photo'),
    path('album/unfavorite/<int:pk>/', views.UnFavoriteAlbumApiView.as_view(), name='unfav_photo'),
]
