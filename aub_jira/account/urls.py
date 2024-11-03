from django.urls import path
from account.views import RegisterUser, LoginUser, UserProfile, UpdateProfile

urlpatterns = [
    path('signup', RegisterUser.as_view(), name='register-user'),
    path('signin', LoginUser.as_view(), name='login-user'),
    path('profile', UserProfile.as_view(), name='my-profile'),
    path('update-profile', UpdateProfile.as_view(), name='update-profile'),
]