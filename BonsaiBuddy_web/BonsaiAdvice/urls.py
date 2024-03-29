from django.urls import path

from . import views

app_name = "BonsaiAdvice"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("technique/<pk>/", views.TechniqueView.as_view(), name="technique_detail"),
    path("objective/<pk>/", views.ObjectiveView.as_view(), name="objective_detail"),
    path("stage/<pk>/", views.StageView.as_view(), name="stage_detail"),
    path("which_technique/", views.WhichTechniqueView.as_view(), name="which_technique"),
]