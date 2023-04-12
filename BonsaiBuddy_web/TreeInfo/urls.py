from django.urls import path, include

from . import views

app_name = "TreeInfo"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.CreateFormView.as_view(), name="create"),
    path("<pk>/", views.DetailView.as_view(), name="detail"),
    path("<pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<pk>/vote/", views.VoteView.as_view(), name="vote"),
]