from django.urls import path
from . import views

app_name = "BonsaiAdmin"
urlpatterns = [
  path("", views.IndexView.as_view(), name="index"),
  path("treeinfo/create", views.CreateTreeInfoFormView.as_view(), name="treeinfo_create", ),
  path("treeinfo/<pk>/update", views.UpdateTreeInfoFormView.as_view(), name="treeinfo_update"),
]
