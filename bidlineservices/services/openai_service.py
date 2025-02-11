from ..openai_client import init_openai

# cs_temperature = 0.7
# cs_top_p = 0.4

async def process_prompt_with_openai(content):
  openai = init_openai()

  try:
    openai_response = await openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": content}]
      # temperature=cs_temperature,
      # top_p=cs_top_p
    )

    openai_response_content = openai_response.choices[0].message.content
    
    # "usage": {
    #   "prompt_tokens": 9,
    #   "completion_tokens": 12,
    #   "total_tokens": 21,
    #   "completion_tokens_details": {
    #     "reasoning_tokens": 0    }
    # }
    # openai_response_usage = openai_response.usage

    openai_response_usage_prompt_tokens = openai_response.usage.prompt_tokens
    openai_response_usage_completion_tokens = openai_response.usage.completion_tokens

    return [
      openai_response_content,
      {
        "prompt_tokens": openai_response_usage_prompt_tokens,
        "completion_tokens": openai_response_usage_completion_tokens
      }
    ]
  except Exception as e:
    print(f"An error occurred while processing with OpenAI: {e}")
    return None

async def process_reminders_prompt_with_openai(content):
  openai = init_openai()

  try:
    openai_response = await openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": content}],
      functions=[
        {
            "name": "extract_dates",
            "parameters": {
                "type": "object",
                "properties": {
                    "dates": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "date": {"type": "string", "description": "Fecha en formato YYYY-MM-DD"},
                                "name": {"type": "string", "description": "Nombre de la fecha o evento"},
                                "description": {"type": "string", "description": "Descripción de la fecha o evento"}
                            },
                            "required": ["date", "name", "description"]
                        }
                    }
                },
                "required": ["dates"]
            }
        }
      ]
    )

    openai_response_content = openai_response.choices[0].message.function_call.arguments

    openai_response_usage_prompt_tokens = openai_response.usage.prompt_tokens
    openai_response_usage_completion_tokens = openai_response.usage.completion_tokens

    return [
      openai_response_content,
      {
        "prompt_tokens": openai_response_usage_prompt_tokens,
        "completion_tokens": openai_response_usage_completion_tokens
      }
    ]
  except Exception as e:
    print(f"An error occurred while processing with OpenAI: {e}")
    return None

async def process_suggested_services_prompt_with_openai(content):
  openai = init_openai()

  try:
    openai_response = await openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": content}],
      functions=[
        {
            "name": "get_suggested_services",
            "parameters": {
                "type": "object",
                "properties": {
                    "suggestedservices": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "number", "description": "Suggested service id"},
                                "name": {"type": "string", "description": "Suggested service name"},
                                "description": {"type": "string", "description": "Suggested service description"}
                            },
                            "required": ["name", "description"]
                        }
                    }
                },
                "required": ["suggestedservices"]
            }
        }
      ]
    )

    openai_response_content = openai_response.choices[0].message.function_call.arguments

    openai_response_usage_prompt_tokens = openai_response.usage.prompt_tokens
    openai_response_usage_completion_tokens = openai_response.usage.completion_tokens

    return [
      openai_response_content,
      {
        "prompt_tokens": openai_response_usage_prompt_tokens,
        "completion_tokens": openai_response_usage_completion_tokens
      }
    ]
  except Exception as e:
    print(f"An error occurred while processing with OpenAI: {e}")
    return None

async def process_suggested_talents_prompt_with_openai(content):
  openai = init_openai()

  try:
    openai_response = await openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": content}],
      functions=[
        {
          "name": "get_suggested_talents",
          "parameters": {
              "type": "object",
              "properties": {
                  "suggestedtalents": {
                      "type": "array",
                      "items": {
                          "type": "object",
                          "properties": {
                              "id": {"type": "number", "description": "Suggested talent/professional id"},
                              "full_name": {"type": "string", "description": "Suggested talent/professional fullname"},
                              "job_title": {"type": "string", "description": "Suggested talent/professional job title"}
                          },
                          "required": ["full_name", "job_title"]
                      }
                  }
              },
              "required": ["suggestedtalents"]
          }
        }
      ]
      # temperature=cs_temperature,
      # top_p=cs_top_p
    )

    print("OPENAI RESPONSE")
    print(openai_response)
    openai_response_content = openai_response.choices[0].message.function_call.arguments

    openai_response_usage_prompt_tokens = openai_response.usage.prompt_tokens
    openai_response_usage_completion_tokens = openai_response.usage.completion_tokens

    return [
      openai_response_content,
      {
        "prompt_tokens": openai_response_usage_prompt_tokens,
        "completion_tokens": openai_response_usage_completion_tokens
      }
    ]
  except Exception as e:
    print(f"An error occurred while processing with OpenAI: {e}")
    return None