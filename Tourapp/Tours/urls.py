from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='categories', viewset=views.CategoryViewSet, basename='category')
router.register(prefix='tours', viewset=views.TourViewSet, basename='tour')
router.register(prefix='news', viewset=views.NewsViewSet, basename='news')
router.register(prefix='customer', viewset=views.CustomerViewSet, basename='customer')
router.register(prefix='employees', viewset=views.EmployeeViewSet, basename='employee')
router.register(prefix='comments', viewset=views.CommentViewSet, basename='comment')
urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view())
]