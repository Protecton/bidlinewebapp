from random import randint
from ..supabase_client import init_supabase

# Función para obtener un prompt desde la tabla 'prompts'
def get_prompt_from_supabase():
  supabase = init_supabase()
  id_to_get = randint(1, 5)
  response = supabase.table("prompts").select("*").eq("id", id_to_get).execute()
  
  if response.data:
    return response.data[0]["content"]
  else:
      return None

def get_function_prompt_from_supabase(function_name):
  try:
    supabase = init_supabase()
    
    response = supabase.table("function_prompts").select("*").eq("function_name", function_name).execute()

    prompt_id = response.data[0]["prompt_id"]

    response2 = supabase.table("prompts").select("*").eq("id", prompt_id).execute()

    if response2.data:
      return response2.data[0]
    else:
      return None
  except Exception as e:
    print(f"An error occurred while processing with Supabase and {function_name}: {e}")
    return None

# Función para guardar la respuesta en la tabla 'openairesponses'
def save_response_to_supabase(prompt, response):
  supabase = init_supabase()
  insert_response = supabase.table("openairesponses").insert({"prompt": prompt, "response": response, "company_id": 1}).execute()
  return bool(insert_response.data)
