from django.urls import path

from . import views

app_name = "Profile"
urlpatterns = [
    path("", views.DetailView.as_view(), name="detail"),
    path("update", views.ProfileUpdateView.as_view(), name="update"),
    path("login", views.MyLoginView.as_view(), name="login"),
    path("signup", views.SignupView.as_view(), name="signup"),
]