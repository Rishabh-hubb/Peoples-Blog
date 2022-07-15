from django.urls import path
from .views import BlogApiView,DetailApiView

urlpatterns = [
    path("",BlogApiView.as_view()),
    path("<int:pk>/",DetailApiView.as_view()),
]