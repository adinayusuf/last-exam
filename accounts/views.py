from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import DetailView


# Create your views here.

class ProfileView(DetailView):
    model = get_user_model()
    template_name = "profile/profile.html"
    context_object_name = "user_object"
    paginate_related_by = 5
    paginate_related_orphans = 0
