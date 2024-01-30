from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('protected/', views.protected_view),
  path('unprotected/', views.unprotected_view),
  path('slice-text/<str:text>', views.bid_slice_text),
  #path('weaviate-connection/', views.weaviate_connection),
  path('create_objects_weaviate/', views.create_class_weaviate),
  path('get_collections/', views.get_collections),
  path('create_db_connection/', views.create_db_connection),
  path('execute_queries/', views.execute_queries),
]
