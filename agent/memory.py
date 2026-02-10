import chromadb
import uuid
from datetime import datetime
from termcolor import colored

# Veritabanını 'chroma_db' klasörüne kaydet (Persistent)
client = chromadb.PersistentClient(path="chroma_db")

# Koleksiyon oluştur (Tablo gibi düşün)
collection = client.get_or_create_collection(name="agent_reports")

def save_to_memory(text, topic):
    """
    Raporu vektör veritabanına kaydeder.
    """
    print(colored(f"💾 MEMORY: Bilgi uzun süreli hafızaya işleniyor...", "blue"))
    
    collection.add(
        documents=[text],
        metadatas=[{"topic": topic, "date": datetime.now().strftime("%Y-%m-%d")}],
        ids=[str(uuid.uuid4())]
    )

def search_memory(query):
    """
    Eski raporlar arasında anlamsal arama yapar.
    Mesafe (Distance) kontrolü ile alakasız sonuçları eler.
    """
    print(colored(f"🧠 MEMORY: Hafıza taranıyor... [{query}]", "blue"))
    
    results = collection.query(
        query_texts=[query],
        n_results=5 
    )
    
    documents = results['documents'][0]
    distances = results['distances'][0] 
    
    if not documents:
        return "Hafızada bu konuyla ilgili bilgi bulunamadı."

    # --- YENİ EKLENEN KISIM: THRESHOLD (EŞİK) KONTROLÜ ---
    # ChromaDB varsayılan (L2) mesafesi kullanır.
    # 0.0 -> Birebir aynı
    # > 1.5 -> Alakasız olabilir (Bu değer deneme yanılma ile bulunur)
    THRESHOLD = 1.5 
    
    valid_docs = []
    
    for doc, dist in zip(documents, distances):
        # Eğer mesafe eşikten küçükse (yani alakalıysa) listeye ekle
        if dist < THRESHOLD:
            valid_docs.append(f"(Benzerlik: {dist:.2f}) - {doc}")
            
    if not valid_docs:
        return "Hafızada kayıtlar var ancak aradığınız konuyla yeterince alakalı değiller."

    context = "HAFIZADAN GELEN BİLGİLER (GEÇMİŞ RAPORLAR):\n"
    for i, doc in enumerate(valid_docs):
        context += f"--- Kayıt {i+1} ---\n{doc}\n"
        
    return context