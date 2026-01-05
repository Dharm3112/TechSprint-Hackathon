import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env")
else:
    print(f"🔑 checking key: {api_key[:5]}...{api_key[-3:]}")
    genai.configure(api_key=api_key)
    
    print("\n📋 Available Models for your Key:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   ✅ {m.name}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")