import weaviate
from decouple import config

def weaviate_connection():
  client = weaviate.Client(
     url = "https://o8rdynkss2uddb4ldicfsg.c0.us-central1.gcp.weaviate.cloud",  # Replace with your endpoint
     auth_client_secret=weaviate.AuthApiKey(config('api_key_weaviate')),  # Replace w/ your Weaviate instance API key
     additional_headers = {
         "X-OpenAI-Api-Key": config('OPENAI_APIKEY')  # Replace with your inference API key
     }
  )


  return client