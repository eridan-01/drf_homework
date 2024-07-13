from django.urls import path

from materials.apps import MaterialsConfig

from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register("", CourseViewSet)

urlpatterns = [
] + router.urls
