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

    # print(openai_response_usage_prompt_tokens)
    # print(openai_response_usage_completion_tokens)

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

    print("OPEN AI RESPONSE")
    print(openai_response)
    
    openai_response_content = openai_response.choices[0].message.function_call.arguments

    # import json
    # arguments_data = json.loads(openai_response_content)
    # dates = arguments_data["dates"]

    # print(dates)  # Imprimirá [] si no hay fechas

    openai_response_usage_prompt_tokens = openai_response.usage.prompt_tokens
    openai_response_usage_completion_tokens = openai_response.usage.completion_tokens

    print("DATES RES")
    print(openai_response_content)

    # {"dates":[{"date":"2025-02-01","name":"Project launch","description":"The planned launch date for the real estate platform."}]}
    # {"dates":[]}

    # ChatCompletion(id='chatcmpl-AORbNhHq7mDzjgrgeAbs0XAzBWTlB', choices=[Choice(finish_reason='function_call', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=FunctionCall(arguments='{"dates":[]}', name='extract_dates'), tool_calls=None, refusal=None))], created=1730389337, model='gpt-4o-mini-2024-07-18', object='chat.completion', system_fingerprint='fp_0ba0d124f1', usage=CompletionUsage(completion_tokens=13, prompt_tokens=681, total_tokens=694, prompt_tokens_details={'cached_tokens': 0}, completion_tokens_details={'reasoning_tokens':
    # ChatCompletion(id='chatcmpl-AOSzZ2UagyzGsVpvUNEriTAJJwU4X', choices=[Choice(finish_reason='function_call', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=FunctionCall(arguments='{"dates":[{"date":"2025-02-01","name":"Platform readiness","description":"Completion of the customizable e-learning platform by the specified due date."}]}', name='extract_dates'), tool_calls=None, refusal=None))], created=1730394681, model='gpt-4o-mini-2024-07-18', object='chat.completion', system_fingerprint='fp_8bfc6a7dc2', usage=CompletionUsage(completion_tokens=44, prompt_tokens=722, total_tokens=766, prompt_tokens_details={'cached_tokens': 0}, completion_tokens_details={'reasoning_tokens': 0}))
    # ChatCompletion(id='chatcmpl-AOT1E1HrtZySstJipDeGeWGG0esUx', choices=[Choice(finish_reason='function_call', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=FunctionCall(arguments='{"dates":[{"date":"2025-02-01","name":"Platform Completion Date","description":"The date by which the e-learning platform should be completed and ready for use."}]}', name='extract_dates'), tool_calls=None, refusal=None))], created=1730394784, model='gpt-4o-mini-2024-07-18', object='chat.completion', system_fingerprint='fp_8bfc6a7dc2', usage=CompletionUsage(completion_tokens=48, prompt_tokens=722, total_tokens=770, prompt_tokens_details={'cached_tokens': 0}, completion_tokens_details={'reasoning_tokens': 0}))
    
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
