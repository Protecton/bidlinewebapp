# openai_client.py
from openai import OpenAI
from django.conf import settings

# Inicializar la conexión con OpenAI
def init_openai():
  client = OpenAI(
    # This is the default and can be omitted
    api_key=settings.OPENAI_APIKEY,
  )
  # openai.api_key = settings.OPENAI_APIKEY
  return client
