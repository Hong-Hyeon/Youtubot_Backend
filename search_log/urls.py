from django.urls import path
from . import views

urlpatterns = [
    path("",views.SearchLog_API.as_view()),
]