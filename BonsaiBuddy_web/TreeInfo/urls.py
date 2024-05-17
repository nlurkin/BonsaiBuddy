from django.urls import include, path

from . import views

app_name = "TreeInfo"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<str:pk>/", views.DetailView.as_view(), name="detail"),
]
