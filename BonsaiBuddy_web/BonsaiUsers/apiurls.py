from django.urls import path, include
from rest_framework_mongoengine import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'users/profile', views.ProfileViewSet, basename='profile')

urlpatterns = [path('', include(router.urls)),
               path('users/profile/<str:username>/password',
                    views.ChangePasswordView.as_view(), name='change_password'),
               path('users/profile/passwordcheck', views.CheckPasswordValidityView.as_view(), name='check_password')]
