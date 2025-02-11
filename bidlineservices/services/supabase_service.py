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

def get_proposal_data_by_id(proposal_id):
  try:
    supabase = init_supabase()
    
    proposal_response = supabase.table("proposals").select("*").eq("id", proposal_id).execute()

    proposal_id = proposal_response.data[0]["id"]
    proposal_company_id = proposal_response.data[0]["company_id"]

    company_response = supabase.table("companies").select("*").eq("id", proposal_company_id).execute()

    company_information = company_response.data[0]["description"]

    past_projects = ""

    past_projects_response = supabase.table("past_projects").select("*").eq("company_id", proposal_company_id).execute()
    
    if past_projects_response.data:
      for past_project in past_projects_response.data:
        past_projects = past_projects + past_project["description"] + " "
    else:
      past_projects = "No past projects found"
    
    request_for_proposal_response = supabase.table("requests_for_proposals").select("*").eq("proposal_id", proposal_id).execute()

    request_for_proposal_prompt = request_for_proposal_response.data[0]["description"]
    request_for_proposal_id = request_for_proposal_response.data[0]["id"]
    
    if not proposal_response.data:
      request_for_proposal_prompt = "No request for proposal"

    if not company_response.data:
      company_information = "No company information found"

    return [
      request_for_proposal_prompt,
      company_information,
      past_projects,
      proposal_company_id,
      request_for_proposal_id
    ]
  except Exception as e:
    print(f"An error occurred while processing with Supabase and getting proposal {proposal_id}: {e}")
    return None

def get_proposal_data_for_suggested_by_id(proposal_id):
  try:
    supabase = init_supabase()
    
    proposal_response = supabase.table("proposals").select("*").eq("id", proposal_id).execute()

    proposal_id = proposal_response.data[0]["id"]
    proposal_company_id = proposal_response.data[0]["company_id"]

    company_response = supabase.table("companies").select("*").eq("id", proposal_company_id).execute()


    company_information = company_response.data[0]["description"]

    past_projects = ""

    past_projects_response = supabase.table("past_projects").select("*").eq("company_id", proposal_company_id).execute()
    
    # product_services = ""

    print(proposal_company_id)

    product_services_response = supabase.table("product_services").select("*").eq("company", proposal_company_id).execute()
    
    talents_response = supabase.table("talents").select("*").eq("company", proposal_company_id).execute()

    if past_projects_response.data:
      for past_project in past_projects_response.data:
        past_projects = past_projects + past_project["description"] + " "
    else:
      past_projects = "No past projects found"

    # if product_services_response.data:
    #   for product_services in product_services_response.data:
    #     product_servicess = product_servicess + product_services["description"] + " "
    # else:
    #   product_servicess = "No product services found"
    
    request_for_proposal_response = supabase.table("requests_for_proposals").select("*").eq("proposal_id", proposal_id).execute()

    request_for_proposal_prompt = request_for_proposal_response.data[0]["description"]
    request_for_proposal_id = request_for_proposal_response.data[0]["id"]
    
    if not proposal_response.data:
      request_for_proposal_prompt = "No request for proposal"

    if not company_response.data:
      company_information = "No company information found"

    print("SERVICES")
    print(product_services_response)

    print("TALENTS")
    print(talents_response)

    return [
      request_for_proposal_prompt,
      company_information,
      past_projects,
      product_services_response.data,
      proposal_company_id,
      request_for_proposal_id,
      talents_response.data
    ]
  except Exception as e:
    print(f"An error occurred while processing with Supabase and getting proposal {proposal_id}: {e}")
    return None

# Función para guardar la respuesta en la tabla 'openairesponses'
def save_response_to_supabase(prompt, response, company_id, prompt_tokens, completion_tokens, proposal_id, prompt_id):
  supabase = init_supabase()
  insert_response = supabase.table("openairesponses").insert({
    "prompt": prompt,
    "response": response,
    "company_id": company_id,
    "prompt_tokens": prompt_tokens,
    "completion_tokens": completion_tokens,
    "proposal_id": proposal_id,
    "prompt_id": prompt_id
  }).execute()
  return bool(insert_response.data)

def save_proposal_content(proposal_id, proposal_content):
  supabase = init_supabase()
  update_response = supabase.table("proposals").update({"description": proposal_content}).eq("id", proposal_id).execute()
  return bool(update_response.data)

def save_proposal_summary(proposal_id, summary_content):
  supabase = init_supabase()
  update_response = supabase.table("proposals").update({"summary": summary_content}).eq("id", proposal_id).execute()
  return bool(update_response.data)

def save_reminder(proposal_id, name, description, reminder_date, request_for_proposal_id):
  supabase = init_supabase()
  insert_response = supabase.table("reminders").insert({
    "proposal_id": proposal_id,
    "user_id": 1,
    "name": name,
    "description": description,
    "reminder_date": reminder_date,
    "requests_for_proposal_id": request_for_proposal_id,
    "status_id": 3
  }).execute()
  return bool(insert_response.data)

def save_suggested_product_services(proposal_id, product_services_id):
  supabase = init_supabase()

  existing = supabase.table("proposal_suggested_product_services").select("id").eq("proposal_id", proposal_id).eq("product_services_id", product_services_id).execute()
  
  if existing.data:
    return False
  
  insert_response = supabase.table("proposal_suggested_product_services").insert({
    "proposal_id": proposal_id,
    "product_services_id": product_services_id
  }).execute()
  return bool(insert_response.data)

def save_suggested_talent(proposal_id, talent_id):
  supabase = init_supabase()

  existing = supabase.table("proposal_suggested_talents").select("id").eq("proposal_id", proposal_id).eq("talent_id", talent_id).execute()
  
  if existing.data:
    return False
  
  insert_response = supabase.table("proposal_suggested_talents").insert({
    "proposal_id": proposal_id,
    "talent_id": talent_id
  }).execute()

  return bool(insert_response.data)

