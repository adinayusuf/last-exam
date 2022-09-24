from django.urls import path, include

from accounts.views import ProfileView

app_name = 'accounts'


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/<int:pk>', ProfileView.as_view(), name='user_profile')
]
