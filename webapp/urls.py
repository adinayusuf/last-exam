from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('photos/create/', views.PhotoCreateView.as_view(), name='photo_create'),
    path('photos/<int:pk>/detail/', views.PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/<int:pk>/update/', views.PhotoUpdateView.as_view(), name='photo_update'),
    path('photos/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),
    path('photos/<int:pk>/link/create/', views.CreatePhotoToken.as_view(), name='create_token'),
    path('photos/link/<uuid:pk>/', views.RetrievePhotoToken.as_view(), name='token_photo'),
    path('albums/list/', views.AlbumListView.as_view(), name='album_list'),
    path('albums/create/', views.AlbumCreateView.as_view(), name='album_create'),
    path('albums/<int:pk>/detail/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('albums/<int:pk>/update/', views.AlbumUpdateView.as_view(), name='album_update'),
    path('albums/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album_delete'),
]
