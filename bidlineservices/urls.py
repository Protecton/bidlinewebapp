from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('protected/', views.protected_view),
  path('unprotected/', views.unprotected_view),
  path('slice-text/<str:text>', views.bid_slice_text),
  # path('weaviate-connection/', views.weaviate_connection),
  path('create_objects_weaviate/', views.create_class_weaviate),
  path('insert-phrase/', views.insert_phrase),
  # path('process-supabase-openai-prompt/', views.process_supabase_openai_prompt),
  path('process-proposal/', views.process_proposal),
  path('process-proposal-suggested/', views.process_proposal_suggested),
  path('get_collections/', views.get_collections),
  path('create_db_connection/', views.create_db_connection),
  path('execute_queries/', views.execute_queries),
  path('verify-fbtoken/', views.verify_firebase_token),
  path('getbyemail-fbuser/', views.get_user_by_email),
  path('create-fbuser/', views.create_new_firebase_user),
  path('update-fbuser/', views.update_firebase_user),
  path('delete-fbuser/', views.delete_firebase_user),
  path('supabase/gettable', views.get_supabase_table),
  path('upload-document/', views.upload_document),
  path('delete-objects/', views.delete_all_rfp_objects),
]
