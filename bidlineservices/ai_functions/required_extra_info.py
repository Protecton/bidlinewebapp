from ..services.supabase_service import get_function_prompt_from_supabase
from ..services.openai_service import process_prompt_with_openai
from ..utils.utils import concatenar_valores

async def required_extra_info_v1(params):
  prompt = get_function_prompt_from_supabase("required_extra_info_v1")

  # print(prompt)

  if not prompt:
    return None

  prompt_number_of_params = prompt["number_of_params"]

  if (len(params) == prompt_number_of_params):
    prompt_content = prompt["content"]

    processed_prompt = concatenar_valores(prompt_content, params)
    
    # Procesar el prompt con OpenAI
    openai_response_content = await process_prompt_with_openai(processed_prompt)
    
    if not openai_response_content:
      return None
    
    return [processed_prompt, openai_response_content]
  else:
    return None
