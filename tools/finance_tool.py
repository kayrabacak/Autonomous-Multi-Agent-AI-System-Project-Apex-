import yfinance as yf
from termcolor import colored

def get_stock_data(symbol):
    """
    Verilen hisse senedi sembolü (veya sembolleri) için son 1 aylık veriyi çeker.
    Girdi: "NVDA" veya "NVDA, AMD" şeklinde olabilir.
    """
    print(colored(f"📈 FINANCE: Veri çekiliyor... [{symbol}]", "blue"))
    
    try:
        # 1. TEMİZLİK: Virgülleri boşluğa çevir ve parçala
        # Örnek: "NVDA, AMD" -> ["NVDA", "AMD"]
        tickers = symbol.replace(",", " ").split()
        
        full_report = ""
        
        # 2. DÖNGÜ: Her bir hisse için tek tek veri çek
        for ticker_symbol in tickers:
            ticker_symbol = ticker_symbol.strip().upper() # Boşlukları sil, büyük harf yap
            if not ticker_symbol:
                continue
                
            stock = yf.Ticker(ticker_symbol)
            hist = stock.history(period="1mo")
            
            if hist.empty:
                full_report += f"\n--- {ticker_symbol} ---\nVeri bulunamadı veya sembol hatalı.\n"
                continue
            
            # Son kapanış fiyatı
            last_price = hist['Close'].iloc[-1]
            # 1 ay önceki fiyat (Başlangıç)
            start_price = hist['Close'].iloc[0]
            # Değişim oranı
            change = ((last_price - start_price) / start_price) * 100
            
            full_report += (
                f"\n--- {ticker_symbol} ---\n"
                f"Güncel Fiyat: ${last_price:.2f}\n"
                f"1 Aylık Değişim: %{change:.2f}\n"
                f"Son 5 Günlük Kapanışlar: {hist['Close'].tail(5).tolist()}\n"
            )
            
        return full_report if full_report else "Hata: Hiçbir sembol için veri çekilemedi."

    except Exception as e:
        return f"Borsa verisi çekilirken hata oluştu: {str(e)}"

# Test için
if __name__ == "__main__":
    print(get_stock_data("NVDA, AMD"))