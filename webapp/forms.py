from django.contrib.admin import forms
from django.contrib.auth import get_user_model

from django import forms
from django.db.models import Q

from webapp.models import Photo, Album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        author_id = None
        if 'author_id' in kwargs:
            author_id = kwargs.pop('author_id')
        super(PhotoForm, self).__init__(*args, **kwargs)
        if author_id:
            user = get_user_model().objects.get(id=author_id)
            self.fields['album'].queryset = user.albums.all()


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        author_id = None
        if 'author_id' in kwargs:
            author_id = kwargs.pop('author_id')
        super(AlbumForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            user = get_user_model().objects.get(id=author_id)
            self.fields['photo'].queryset = self.instance.photo_set.filter(Q(is_private=False) | Q(author=user))
