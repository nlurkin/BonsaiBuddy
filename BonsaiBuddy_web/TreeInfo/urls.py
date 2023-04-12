from django.urls import path, include

from . import views

app_name = "TreeInfo"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<pk>/", views.DetailView.as_view(), name="detail"),
]