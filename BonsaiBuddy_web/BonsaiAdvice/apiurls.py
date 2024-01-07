from django.urls import path, include
from rest_framework_mongoengine import routers

from . import views

router = routers.DefaultRouter()
router.register(r'advices', views.BonsaiTechniqueViewSet,
                basename='techniques')

urlpatterns = [path('', include(router.urls)), path(
    'advices/techniques_categories', views.BonsaiTechniqueCategoriesView.as_view())]
