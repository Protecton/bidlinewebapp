from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('protected/', views.protected_view),
  path('unprotected/', views.unprotected_view),
  path('slice-text/', views.bid_slice_text),
]
