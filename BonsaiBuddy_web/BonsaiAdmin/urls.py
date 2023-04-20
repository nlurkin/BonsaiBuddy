from django.urls import path
from . import views

app_name = "BonsaiAdmin"
urlpatterns = [
  path("", views.IndexView.as_view(), name="index"),
  path("treeinfo/create", views.TreeInfoFormView.as_view(), name="treeinfo_create", ),
  path("treeinfo/<pk>/update", views.TreeInfoFormView.as_view(), name="treeinfo_update"),
  path("technique/create", views.BonsaiTechniqueFormView.as_view(), name="technique_create"),
  path("technique/<pk>/update", views.BonsaiTechniqueFormView.as_view(), name="technique_update"),
  path("objective/create", views.BonsaiObjectiveFormView.as_view(), name="objective_create"),
  path("objective/<pk>/update", views.BonsaiObjectiveFormView.as_view(), name="objective_update"),
]
