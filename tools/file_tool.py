import os
import PyPDF2
from termcolor import colored

def read_local_file(file_path):
    """
    Verilen dosya yolundaki PDF veya TXT dosyasını okur.
    """
    print(colored(f"📂 FILE: Dosya okunuyor... [{file_path}]", "magenta"))
    
    if not os.path.exists(file_path):
        return "HATA: Dosya bulunamadı. Lütfen dosya yolunu kontrol et."

    try:
        content = ""
        # PDF Okuma
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content += page.extract_text() + "\n"
        
        # TXT/MD/CSV Okuma
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
        # Çok uzunsa kısaltalım (Token limitine takılmamak için)
        if len(content) > 10000:
            return content[:10000] + "\n...[Dosya çok uzun, ilk 10.000 karakter alındı]..."
            
        return content

    except Exception as e:
        return f"Dosya okuma hatası: {str(e)}"

if __name__ == "__main__":
    # Test için bir dosya yolu verilebilir
    pass