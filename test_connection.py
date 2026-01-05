import google.generativeai as genai
import os

# Paste your key here (or better, use os.getenv("GEMINI_API_KEY"))
API_KEY = "AIzaSyDlAvbPNL19QColAz4N4QtFGEUcHgvzSQQ"

# Configure the library
genai.configure(api_key=API_KEY)

# Initialize Model
model = genai.GenerativeModel('gemini-1.5-flash')

print("📨 Sending test message...")
response = model.generate_content("Are you online?")
print(f"✅ SUCCESS: {response.text}")