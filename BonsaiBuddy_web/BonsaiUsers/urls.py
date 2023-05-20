from django.urls import path

from . import views

app_name = "Profile"
urlpatterns = [
    path("", views.DetailView.as_view(), name="detail"),
    path("update/", views.ProfileUpdateView.as_view(), name="update"),
    path("my_trees/", views.MyTreesListView.as_view(), name="my_trees"),
    path("my_trees/create", views.MyTreesFormView.as_view(), name="my_trees_create"),
    path("my_trees/<pk>/update", views.MyTreesFormView.as_view(), name="my_trees_update"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("password_change/", views.ModifyPasswordView.as_view(), name="mod_pwd"),
]