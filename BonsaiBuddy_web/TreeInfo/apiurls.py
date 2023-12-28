from django.urls import path, include
from rest_framework_mongoengine import routers

from . import views

router = routers.DefaultRouter()
router.register(r'trees', views.TreeInfoViewSet, basename='trees')

urlpatterns = [path('', include(router.urls))]
