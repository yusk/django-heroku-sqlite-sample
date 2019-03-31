from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('signup', views.SignupView.as_view(), name="signup"),
    path('users/<str:id>', views.UsersView.as_view(), name="users"),
    path('close', views.CloseView.as_view(), name="close"),
]