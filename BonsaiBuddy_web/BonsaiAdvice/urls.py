from django.urls import path

from . import views

app_name = "BonsaiAdvice"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("technique/<pk>", views.TechniqueView.as_view(), name="technique_detail"),
    path("objective/<pk>", views.ObjectiveView.as_view(), name="objective_detail"),
]