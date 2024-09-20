# supabase_client.py
from supabase import create_client, Client
from django.conf import settings

# Inicializar el cliente de Supabase
def init_supabase() -> Client:
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_API_KEY
    supabase = create_client(url, key)
    return supabase