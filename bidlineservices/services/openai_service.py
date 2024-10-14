from ..openai_client import init_openai

async def process_prompt_with_openai(content):
  openai = init_openai()

  try:
    openai_response = await openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": content}]
    )

    openai_response_content = openai_response.choices[0].message.content

    return openai_response_content
  except Exception as e:
    print(f"An error occurred while processing with OpenAI: {e}")
    return None
