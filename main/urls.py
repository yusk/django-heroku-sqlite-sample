from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('close/', views.CloseView.as_view(), name="close"),
]