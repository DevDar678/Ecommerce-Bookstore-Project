
from django.urls import path
from .views import SignUpView
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('accounts/', SignUpView.as_view(), name = 'signup'),
    path('logout/', views.logout_user, name='logout'),
]


