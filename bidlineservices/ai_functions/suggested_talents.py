from ..services.supabase_service import get_function_prompt_from_supabase
from ..services.openai_service import process_suggested_talents_prompt_with_openai
from ..utils.utils import concatenar_valores

async def suggested_talents_v1(params):
  # PARAMS:
  # {
  #   "$$$1": "request_for_proposal",
  #   "$$$2": "company_info",
  #   "$$$3": "action_plan",
  #   "$$$4": "past_projects",
  #   "$$$5": "past_projects_applied",
  #   "$$$6": "proposal_intro",
  #   "$$$7": "services_suggested",
  #   "$$$8": "talents_input",
  #   "$$$9": "request_for_proposal"
  # }
  prompt = get_function_prompt_from_supabase("suggested_talents_v1")

  if not prompt:
    return None

  prompt_number_of_params = prompt["number_of_params"]

  if (len(params) == prompt_number_of_params):
    prompt_id = prompt["id"]
    prompt_content = prompt["content"]

    processed_prompt = concatenar_valores(prompt_content, params)
    # print("PROCESSED PROMPT")
    # print(processed_prompt)
    openai_response_content = await process_suggested_talents_prompt_with_openai(processed_prompt)

    # print("TALENT RESPONSE")
    # print(openai_response_content)

    if not openai_response_content:
      return None
    
    return [processed_prompt, openai_response_content, prompt_id]
  else:
    return None
