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

    # print("REQ FOR PROPOSAL")
    # print(request_for_proposal_prompt)
    # print("COMPANY INFO")
    # print(company_information)
    # print("PAST PROJECTS")
    # print(past_projects)

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