from ..openai_client import init_openai

async def process_prompt_with_openai(content):
  openai = init_openai()

  try:
    openai_response = await openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": content}]
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

    print(openai_response_usage_prompt_tokens)
    print(openai_response_usage_completion_tokens)
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
