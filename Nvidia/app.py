from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Get API key and clean it
os.environ['NVIDIA_API_KEY']=os.getenv("NVIDIA_API_KEY")
nvidia_api_key=os.getenv("NVIDIA_API_KEY")

# Validate API key
if not nvidia_api_key:
    raise ValueError("NVIDIA_API_KEY not found in environment variables")

print(f"Using API key: {nvidia_api_key[:20]}...")  # Chỉ hiện 20 ký tự đầu


client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = nvidia_api_key, 
)

completion = client.chat.completions.create(
  model="meta/llama3-8b-instruct",
  messages=[{"role":"user","content":"hello, how are you?"}],
  temperature=0.5,
  top_p=1,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

