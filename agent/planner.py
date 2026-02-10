# agent/planner.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class Planner:
    def __init__(self):
        # Planner için daha hızlı ve zeki model
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        # --- BURASI DÜZELTİLDİ: AGRESIF ARAŞTIRMACI PROMPTU ---
        self.system_prompt = """
        You are a STRATEGIC TASK PLANNER for an autonomous AI research agent.
        Your goal is to create a direct, execution-oriented plan to satisfy the user's request immediately.

        CRITICAL RULES (FOLLOW STRICTLY):
        1. **NO INTERACTION:** Do NOT create steps that ask the user for clarification, preference, or permission. The agent must act autonomously.
        2. **NO CONDITIONAL STEPS:** Do NOT say "If X is not found, do Y". Assume you will find relevant information (even if it's rumors, leaks, or estimates).
        3. **TARGET RUMORS:** If a product (like Galaxy S26) is not released, your plan MUST be to find "leaks", "rumors", and "expectations". Do NOT plan to just say "it's not released".
        4. **SINGLE REPORT:** The final step MUST ALWAYS be "analyze_data" to compile ONE comprehensive report. Do not create intermediate reporting steps.
        5. **USE MEMORY:** Always start by checking memory.

        JSON FORMAT ONLY:
        {
             "plan": [
               "Check memory for X...",
               "Search internet for X rumors and leaks...",
               "Search internet for X release date estimates...",
               "Compile all gathered info into a final report about X"
             ]
        }
        """

    def create_plan(self, user_goal):
        """
        Kullanıcı hedefini alır ve adım adım plana dönüştürür.
        """
        prompt = f"{self.system_prompt}\n\nUSER GOAL: {user_goal}"
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            # JSON temizliği
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text)["plan"]
            
        except Exception as e:
            print(f"Planner Hatası: {e}")
            # Hata durumunda varsayılan bir plan dön
            return [
                f"Search memory for {user_goal}",
                f"Search internet for {user_goal}",
                f"Analyze and summarize findings about {user_goal}"
            ]

if __name__ == "__main__":
    planner = Planner()
    plan = planner.create_plan("Samsung Galaxy S26 özellikleri")
    print(plan)