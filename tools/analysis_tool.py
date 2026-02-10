import os
import google.generativeai as genai
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Analiz için aynı modeli kullanabiliriz
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"temperature": 0.2}
)

def analyze_content(context, goal):
    """
    Toplanan ham veriyi LLM kullanarak analiz eder ve özetler.
    """
    print(colored(f"🧠 ANALYZER: Veriler işleniyor... Hedef: {goal}", "magenta"))
    
    prompt = f"""
    You are an expert data analyst. 
    
    USER GOAL: {goal}
    
    COLLECTED DATA (CONTEXT):
    {context}
    
    INSTRUCTIONS:
    1. Analyze the collected data carefully.
    2. Ignore irrelevant parts (like navigation menus, ads).
    3. Synthesize the information to answer the User Goal directly.
    4. Provide a professional, well-structured report in TURKISH.
    5. Cite dates or specific numbers if available.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Analiz hatası: {str(e)}"