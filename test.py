import openai
from configuration import apikey  # Adjusted based on your folder structure

openai.api_key = apikey
try:
  response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt="write a letter for my resignation",
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  print(response)
except openai.error.RateLimitError:
  print("Rate limit exceeded. Please try again later or check your OpenAI API plan.")