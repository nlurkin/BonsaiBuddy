from django.urls import path, include
from rest_framework_mongoengine import routers

from . import views

router = routers.DefaultRouter()
router.register(r'advices/techniques', views.BonsaiTechniqueViewSet,
                basename='techniques')
router.register(r'advices/objectives', views.BonsaiObjectiveViewSet,
                basename='objectives')
router.register(r'advices/stages', views.BonsaiStageViewSet,
                basename='stages')

urlpatterns = [path('', include(router.urls)),
               path('advices/techniques_categories',
                    views.BonsaiTechniqueCategoriesView.as_view()),
               path('advices/association_search',
                    views.AssociationSearchView.as_view()),
               ]
