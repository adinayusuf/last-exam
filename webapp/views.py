from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm, AlbumForm
from webapp.models import Photo, Album, PhotoToken


class IndexView(ListView):
    model = Photo
    template_name = 'index.html'
    context_object_name = 'photos'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Photo.objects.filter(Q(is_private=False) | Q(author=self.request.user)).order_by("-created_at")
        return Photo.objects.filter(is_private=False).order_by("-created_at")


class PhotoDetailView(DetailView):
    template_name = "photo/detail.html"
    model = Photo
    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photo/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author_id'] = self.request.user.id
        return kwargs

    def get_success_url(self):
        return reverse("webapp:photo_detail", kwargs={"pk": self.object.pk})


class PhotoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Photo
    context_object_name = 'photo'
    template_name = 'photo/update.html'
    form_class = PhotoForm

    def get_success_url(self):
        return reverse("webapp:photo_detail", kwargs={"pk": self.object.pk})

    def has_permission(self):
        album = self.get_object()
        if album.author == self.request.user:
            return True
        elif self.request.user.has_perm('webapp.change_album'):
            return True
        return False


class PhotoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photo/delete.html'
    success_url = reverse_lazy('webapp:index')

    def has_permission(self):
        album = self.get_object()
        if album.author == self.request.user:
            return True
        elif self.request.user.has_perm('webapp.delete_photo'):
            return True
        return False


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = "album/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:album_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author_id'] = self.request.user.id
        return kwargs


class AlbumUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Album
    context_object_name = 'album'
    template_name = 'album/update.html'
    form_class = AlbumForm

    def get_success_url(self):
        return reverse("webapp:album_detail", kwargs={"pk": self.object.pk})

    def has_permission(self):
        album = self.get_object()
        if album.author == self.request.user:
            return True
        elif self.request.user.has_perm('webapp.change_album'):
            return True
        return False


class AlbumListView(ListView):
    model = Album
    context_object_name = 'albums'
    queryset = Album.objects.none()
    template_name = 'album/list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Album.objects.filter(Q(is_private=False) | Q(author=self.request.user)).order_by("-created_at")
        return Album.objects.filter(is_private=False).order_by("-created_at")


class AlbumDetailView(DetailView):
    template_name = "album/detail.html"
    model = Album
    context_object_name = 'album'


class AlbumDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Album
    template_name = 'album/delete.html'
    success_url = reverse_lazy('webapp:album_list')

    def has_permission(self):
        album = self.get_object()
        if album.author == self.request.user:
            return True
        elif self.request.user.has_perm('webapp.delete_album'):
            return True
        return False


class CreatePhotoToken(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        photo = self.get_object()
        PhotoToken.objects.create(photo=photo)
        return redirect('webapp:photo_detail', pk=photo.id)

    def has_permission(self):
        photo = self.get_object()
        if photo.author == self.request.user:
            return True
        return False

    def get_object(self):
        return Photo.objects.get(id=self.kwargs.get('pk'))


class RetrievePhotoToken(DetailView):
    model = PhotoToken
    template_name = "photo/detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.expires > timezone.now():
            context = {'photo': self.object.photo}
            return self.render_to_response(context)
        return HttpResponseForbidden()
