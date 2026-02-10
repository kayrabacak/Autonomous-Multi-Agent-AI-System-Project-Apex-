import sys
import io
import os
# --- DEĞİŞİKLİK BAŞLANGICI ---
import matplotlib
matplotlib.use('Agg')  # Arayüz (GUI) yok, sadece dosya oluştur diyoruz.
import matplotlib.pyplot as plt
# --- DEĞİŞİKLİK BİTİŞİ ---
from termcolor import colored


# Grafikleri kaydedeceğimiz klasör
if not os.path.exists("charts"):
    os.makedirs("charts")

def execute_python_code(code):
    """
    LLM tarafından üretilen Python kodunu çalıştırır.
    Matematiksel sonuçları ve oluşturulan grafik dosyalarının yollarını döner.
    """
    print(colored(f"🐍 PYTHON: Kod çalıştırılıyor...", "magenta"))
    
    # Standart çıktıyı (print) yakalamak için
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # Kodun içindeki plt.show() komutlarını plt.savefig() ile değiştirelim
        # Böylece ekrana pencere açmak yerine dosyaya kaydeder.
        if "plt.plot" in code or "matplotlib" in code:
            import uuid
            filename = f"charts/chart_{uuid.uuid4().hex[:8]}.png"
            code += f"\nplt.savefig('{filename}')\nprint('Grafik oluşturuldu: {filename}')\nplt.close()"
        
        # Kodu çalıştır (Exec tehlikelidir ama lokalde sorun yok)
        exec(code, globals())
        
        # Çıktıyı al
        output = redirected_output.getvalue()
        return output if output else "Kod çalıştı ama çıktı üretmedi (print kullan)."

    except Exception as e:
        return f"Kod Hatası: {str(e)}"
    finally:
        sys.stdout = old_stdout # Çıktıyı normale döndür

# Test
if __name__ == "__main__":
    code = """
import matplotlib.pyplot as plt
x = [1, 2, 3]
y = [10, 20, 5]
plt.plot(x, y)
plt.title("Test Grafiği")
"""
    print(execute_python_code(code))