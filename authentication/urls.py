from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.login_view, name='my_login'),
    path('logout/', LogoutView.as_view(), name='my_logout'),
]
