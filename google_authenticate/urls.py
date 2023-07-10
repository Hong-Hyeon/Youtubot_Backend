from django.urls import path
from . import views

urlpatterns = [
    path("",views.GoogleAuthenticate_API.as_view()),
]