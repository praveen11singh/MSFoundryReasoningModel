
from openai import OpenAI
import os
import re
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(  
  base_url = os.environ["endpoint"], 
  api_key=token_provider,
)
response = client.chat.completions.create(
  model=os.environ["deployment_name"], # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "How many languages are in the Bihar?"}
  ],
  max_tokens=10000  # Limit response length
)

#print(response.choices[0].message)

# To get detail expmanation
#print(response.model_dump_json(indent=2))

# To get less response, you can set max_tokens to a smaller value, e.g., 100 or 200.
match = re.match(r"<think>(.*?)</think>(.*)", response.choices[0].message.content, re.DOTALL)

print("Response:")
if match:
    print("\tThinking:", match.group(1))
    print("\tAnswer:", match.group(2))
else:
    print("\tAnswer:", response.choices[0].message.content)
print("Model:", response.model)
print("Usage:")
print("\tPrompt tokens:", response.usage.prompt_tokens)
print("\tTotal tokens:", response.usage.total_tokens)
print("\tCompletion tokens:", response.usage.completion_tokens)
