# Autonomous Multi-Agent AI System (Project Apex)

**Project Apex**, kullanıcı hedeflerini gerçekleştirmek için otonom olarak planlama yapan, internet araştırması yürüten, veri analizi sağlayan ve kod yazabilen gelişmiş bir yapay zeka ajanıdır. Google'ın **Gemini 2.5 Flash** modelini temel alır ve **Tavily API** ile gerçek zamanlı internet erişimine sahiptir.

## 🚀 Özellikler

*   **Otonom Görev Planlama:** Kullanıcının verdiği hedefi analiz eder ve adım adım uygulanabilir bir plana dönüştürür.
*   **İnternet Araştırması:** Tavily API kullanarak internetten güncel bilgileri toplar ve analiz eder.
*   **Hafıza Yönetimi:** Öğrenilen bilgileri ve geçmiş görevleri hafızasında tutarak gereksiz tekrarları önler.
*   **Finansal Analiz:** Borsa verilerini çekip analiz edebilir (örneğin: hisse senedi karşılaştırmaları).
*   **Kod Çalıştırma:** Python kodu yazıp yürüterek matematiksel işlemler, veri görselleştirme ve karmaşık analizler yapabilir.
*   **Modern Arayüz:** React ve Vite ile geliştirilmiş, kullanıcı dostu bir web arayüzü sunar.

## 🛠️ Teknolojiler

*   **Backend:** Python, FastAPI
*   **AI Model:** Google Gemini 2.5 Flash
*   **Web Search:** Tavily API
*   **Frontend:** React, Vite, Tailwind CSS (impled via CSS Modules/Custom CSS)
*   **Veri Tabanı:** ChromaDB (Vektör tabanlı hafıza için)

## 📦 Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler

*   Python 3.8 veya üzeri
*   Node.js ve npm

### Adım 1: Projeyi Klonlayın

```bash
git clone https://github.com/kayrabacak/Autonomous-Multi-Agent-AI-System-Project-Apex-.git
cd Autonomous-Multi-Agent-AI-System-Project-Apex-
```

### Adım 2: Backend Kurulumu

Gerekli Python paketlerini yükleyin:

```bash
pip install -r requirements.txt
```

### Adım 3: Çevresel Değişkenler (.env)

Proje kök dizininde bir `.env` dosyası oluşturun ve API anahtarlarınızı ekleyin:

```env
GEMINI_API_KEY=sizin_gemini_api_anahtariniz
TAVILY_API_KEY=sizin_tavily_api_anahtariniz
```

### Adım 4: Frontend Kurulumu

Frontend klasörüne gidin ve bağımlılıkları yükleyin:

```bash
cd frontend
npm install
```

## ▶️ Kullanım

Uygulamayı çalıştırmak için iki ayrı terminal kullanmanız gerekmektedir.

### Backend'i Başlatma

Ana proje dizininde:

```bash
uvicorn api.main:app --reload
```
Bu komut, API sunucusunu `http://127.0.0.1:8000` adresinde başlatır.

### Frontend'i Başlatma

Frontend dizininde:

```bash
npm run dev
```
Bu komut, arayüzü `http://localhost:5173` (veya benzeri bir portta) başlatır. Tarayıcınızda bu adrese giderek ajanı kullanmaya başlayabilirsiniz.
