from django.urls import path
from .views import *


urlpatterns = [
    path("register/", Register.as_view()),
    path("varify/", Varify.as_view()),
]