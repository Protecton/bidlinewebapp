from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('protected/', views.protected_view),
]
