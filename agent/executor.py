import os
import json
import time
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from termcolor import colored
from agent.state import AgentState

# Tools
from tools.search_tool import search_internet
from tools.analysis_tool import analyze_content
from tools.finance_tool import get_stock_data
from tools.coding_tool import execute_python_code
from tools.file_tool import read_local_file
from agent.memory import save_to_memory, search_memory

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# --- AYARLAR ---
MODEL_NAME = "gemini-2.5-flash"

generation_config = {
    "temperature": 0.1,
    "response_mime_type": "application/json",
}

class Executor:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=generation_config
        )
        
        self.system_prompt = """
        You are an intelligent autonomous agent. Select the correct tool for the CURRENT STEP.
        
        AVAILABLE TOOLS:
        1. web_search(query): Use for general online info, news & qualitative analysis.
        2. search_memory(query): ALWAYS use this FIRST to check if we already researched this topic.
        3. read_local_file(file_path): Use to read PDF/TXT files.
        4. get_stock_data(symbol): PRIMARY TOOL for stock data.
           - INPUT RULE: STRICTLY send ONLY the ticker symbols separated by comma.
           - BAD INPUT: "AAPL, compare percentage" OR "AAPL, 1 month"
           - GOOD INPUT: "AAPL, MSFT, GOOG"
        5. execute_python_code(code): Use for MATH, plotting graphs, or data analysis.
        6. analyze_data(data): Use for summarizing info into a final report.
        
        INPUT FORMAT:
        Current Step: [The task]
        Context: [Previous findings]
        
        OUTPUT FORMAT (JSON ONLY):
        {
            "tool_name": "tool_name",
            "tool_input": "input"
        }
        """

    def execute_step(self, current_step, context):
        """
        Şu anki adım için LLM'den bir aksiyon ister.
        Hata durumunda (Quota veya JSON Hatası) bekleyip tekrar dener.
        """
        print(colored(f"⚙️ EXECUTOR: Karar veriliyor... [{current_step}]", "yellow"))
        
        prompt = f"{self.system_prompt}\n\nCurrent Step: {current_step}\nContext: {str(context)}"
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                raw_text = response.text.strip()
                
                # 1. Markdown Temizliği
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()
                
                # 2. JSON Parse ve Windows Path Temizliği
                try:
                    action = json.loads(raw_text)
                except json.JSONDecodeError:
                    print(colored("⚠️ JSON Hatası (Windows path?), temizleniyor...", "yellow"))
                    clean_text = raw_text.replace("\\", "/")
                    action = json.loads(clean_text)

                return action

            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "Quota exceeded" in error_msg:
                    wait_time = 60
                    print(colored(f"⏳ KOTA LİMİTİ! {wait_time} saniye bekleniyor...", "red"))
                    time.sleep(wait_time)
                else:
                    print(colored(f"❌ EXECUTOR ERROR: {e} - Tekrar deneniyor...", "red"))
                    time.sleep(2)
        
        print(colored("❌ Tüm denemeler başarısız oldu.", "red"))
        return None

# --- API İÇİN ANA FONKSİYON ---
def run_agent(user_goal: str):
    """
    API tarafından çağrılacak ana fonksiyon.
    """
    from agent.planner import Planner
    
    # 1. Planlama
    planner = Planner()
    state = AgentState()
    
    print(colored(f"\n🚀 AJAN BAŞLATILDI: {user_goal}", "green"))
    state.plan = planner.create_plan(user_goal)
    
    if not state.plan:
        return {"status": "error", "message": "Plan oluşturulamadı."}

    # 2. Döngü (Execution)
    executor = Executor()
    final_report = ""
    generated_files = [] 

    while True:
        current_step = state.get_current_step()
        if not current_step:
            break
            
        action = executor.execute_step(current_step, state.memory)
        
        if action:
            tool_name = action.get("tool_name")
            tool_input = action.get("tool_input")
            
            # --- DEBUG LOG (SORUNU ÇÖZECEK KISIM) ---
            print(colored(f"🤖 Karar: {tool_name} -> {tool_input}", "cyan"))
            
            result = None
            
            # --- TOOL YÖNLENDİRME ---
            if tool_name == "web_search":
                result = search_internet(tool_input)
            
            elif tool_name == "search_memory":
                # Hafızayı ara
                mem_result = search_memory(tool_input)
                
                # AKILLI REFLEKS: Eğer hafızada yoksa, internete çık!
                if "bulunamadı" in mem_result.lower():
                    print(colored("⚠️ Hafızada yok, otomatik olarak İnternet'e çıkılıyor...", "yellow"))
                    result = search_internet(tool_input)
                else:
                    result = mem_result
                
            elif tool_name == "read_local_file":
                result = read_local_file(tool_input)
            elif tool_name == "get_stock_data":
                result = get_stock_data(tool_input)
            elif tool_name == "execute_python_code":
                result = execute_python_code(tool_input)
            elif tool_name == "analyze_data" or tool_name == "final_answer":
                full_context = str(state.memory) 
                result = analyze_content(full_context, current_step)
                
                # Raporu Dosyaya Kaydet
                if not os.path.exists("reports"):
                    os.makedirs("reports")
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"reports/rapor_{timestamp}.md"
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(result)
                
                # Hafızaya Kaydet (Öğrenme)
                save_to_memory(result, topic=user_goal)
                
                final_report = result
                generated_files.append(filename)
                print(colored(f"💾 Rapor kaydedildi: {filename}", "green"))
            
            # --- BİLİNMEYEN TOOL HATASI İÇİN ---
            else:
                print(colored(f"❌ HATA: Bilinmeyen tool ismi seçildi: '{tool_name}'", "red"))
                result = f"Error: Tool '{tool_name}' not found. Please use exact tool names like 'web_search'."
            
            state.update_memory(f"step_{state.current_step_index}_result", result)
            state.next_step()
        else:
            break
            
    return {
        "status": "success",
        "goal": user_goal,
        "report": final_report,
        "files": generated_files
    }