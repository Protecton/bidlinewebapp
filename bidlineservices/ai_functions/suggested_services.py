from ..services.supabase_service import get_function_prompt_from_supabase
from ..services.openai_service import process_suggested_services_prompt_with_openai
from ..utils.utils import concatenar_valores

async def suggested_services_v1(params):
  # PARAMS:
  # {
  #   "$$$1": "request_for_proposal",
  #   "$$$2": "company_info",
  #   "$$$3": "action_plan",
  #   "$$$4": "past_projects",
  #   "$$$5": "past_projects_applied",
  #   "$$$6": "proposal_intro",
  #   "$$$7": "services",
  #   "$$$8": "request_for_proposal"
  # }
  prompt = get_function_prompt_from_supabase("suggested_services_v1")

  # print(prompt)

  if not prompt:
    return None

  prompt_number_of_params = prompt["number_of_params"]

  if (len(params) == prompt_number_of_params):
    prompt_id = prompt["id"]
    prompt_content = prompt["content"]

    processed_prompt = concatenar_valores(prompt_content, params)
    # print("PROCESSED SERVICES PROMPT PROMPT")
    # print(processed_prompt)
    # Procesar el prompt con OpenAI
    openai_response_content = await process_suggested_services_prompt_with_openai(processed_prompt)
    
    if not openai_response_content:
      return None
    
    return [processed_prompt, openai_response_content, prompt_id]
  else:
    return None
