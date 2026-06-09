from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"

print("ENV PATH =", env_path)
print("FILE EXISTS =", env_path.exists())

load_dotenv(dotenv_path=env_path)

key = os.getenv("GEMINI_API_KEY")
print("KEY =", key)

client = genai.Client(api_key=key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello"
)

print(response.text)