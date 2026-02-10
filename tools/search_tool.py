import os
from tavily import TavilyClient
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()

# İstemciyi başlat
tavily_api_key = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=tavily_api_key)

def search_internet(query):
    """
    İnternette arama yapar ve AI için optimize edilmiş kısa sonuçlar döner.
    """
    print(colored(f"🌍 TAVILY: İnternet taranıyor... [{query}]", "magenta"))
    
    try:
        # search_depth="advanced" daha derin arama yapar
        response = client.search(query, search_depth="advanced", max_results=3)
        
        # Sonuçları metin haline getirelim
        context = ""
        for result in response.get('results', []):
            context += f"\nSource: {result['title']}\nContent: {result['content']}\nUrl: {result['url']}\n---"
            
        return context
    except Exception as e:
        print(colored(f"❌ SEARCH ERROR: {e}", "red"))
        return "Search failed."

# Test etmek için (Doğrudan çalıştırıldığında)
if __name__ == "__main__":
    print(search_internet("Who is the CEO of NVIDIA in 2024?"))