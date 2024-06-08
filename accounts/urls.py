from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/login/', obtain_auth_token, name='token_login'),
    path('token/logout/', LogoutView.as_view(), name='token_logout')
]
