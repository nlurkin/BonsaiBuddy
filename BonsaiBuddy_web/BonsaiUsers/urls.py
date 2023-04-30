from django.urls import path

from . import views

app_name = "Profile"
urlpatterns = [
    path("", views.DetailView.as_view(), name="detail"),
    path("signup", views.SignupView.as_view(), name="signup"),
]