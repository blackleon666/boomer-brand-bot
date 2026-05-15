import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json

# ============================================================================
# BOOMER BRAND AI SISTEMI - YENI VERSIYON
# ============================================================================

WHATSAPP_LINK = "https://wa.me/boomermerter"
INSTAGRAM_LINK = "https://www.instagram.com/boomermerter/"
TELEGRAM_LINK = "@Boomerbrandd"

# API Key'yi config'den al
try:
    from config import HF_API_KEY
except:
    HF_API_KEY = None

def generate(prompt, user_id=None):
    """Ana generate fonksiyonu - API'ye bagli olmadan calisir"""
    
    print(f"[AI] Processing: {prompt}")
    
    # HuggingFace API test et
    ai_response = get_huggingface_response(prompt)
    
    if ai_response:
        return ai_response
    
    # Fallback - yerli yedek yanitlar
    return get_local_response(prompt)

def get_huggingface_response(prompt):
    """HuggingFace API ile yanit al"""
    
    if not HF_API_KEY or HF_API_KEY == "":
        print("[AI] No API key, using local responses")
        return None
    
    # Farkli modelleri dene
    models = [
        "microsoft/phi-2",  # Daha kucuk ama hizli
        "google/flan-t5-small",  # Guvenilir
        "facebook/opt-125m",  # Çok hizli
    ]
    
    for model in models:
        try:
            print(f"[AI] Trying model: {model}")
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            
            full_prompt = f"""Sen Boomer Brand markasinin yapay zeka müsteri temsilcisisin. 
Kisa ve net yanit ver.
Soru: {prompt}
Yanit:"""
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.5
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "").strip()
                    if text and len(text) > 5:
                        print(f"[AI] Success from {model}")
                        return clean_response(text)
                        
        except Exception as e:
            print(f"[AI] {model} error: {e}")
            continue
    
    print("[AI] All models failed, using local responses")
    return None

def clean_response(text):
    """Yanıtı temizle"""
    if not text:
        return None
    
    # Prompt kısmını kaldır
    if "Yanit:" in text:
        text = text.split("Yanit:")[-1].strip()
    if "Answer:" in text:
        text = text.split("Answer:")[-1].strip()
    
    # Temizle
    text = text.strip()
    if len(text) > 300:
        text = text[:297] + "..."
    
    return text

def get_local_response(prompt):
    """Yerli yedek yanitlar"""
    p = prompt.lower()
    
    # Selamlama
    if any(w in p for w in ["merhaba", "selam", "hi", "naber", "nasilsin", "hello"]):
        return "Merhaba! Boomer Brand musteri temsilcisiyim. Size nasil yardimci olabilirim? Urunler icin /katalog yazabilirsiniz."
    
    # Fiyat
    if any(w in p for w in ["fiyat", "kac", "ucret", "ne kadar", "para", "tl", "lira"]):
        return f"Guncel fiyatlar icin WhatsApp uzerinden iletisime gecebilirsiniz: {WHATSAPP_LINK}"
    
    # Kampanya
    if any(w in p for w in ["kampanya", "indirim", "yuzde", "promo", "indirim"]):
        return f"Aktif kampanyalar icin WhatsApp: {WHATSAPP_LINK}"
    
    # Siparis
    if any(w in p for w in ["siparis", " satin", "almak", "vermek", "order"]):
        return f"Siparis vermek icin WhatsApp: {WHATSAPP_LINK}. Urunler icin /katalog yazabilirsiniz."
    
    # Sikayet
    if any(w in p for w in ["sikayet", "iade", "sorun", "problem", "sikayetim"]):
        return "Sikayetinizi dinlemek icin buradayim. Detaylar icin WhatsApp: {WHATSAPP_LINK}. /sikayet yazarak da bildirebilirsiniz."
    
    # Urun
    if any(w in p for w in ["urun", "urunler", "katalog", "ne var", "neler var", "giyim"]):
        return "Urunlerimizi gormek icin /katalog yazabilirsiniz. Detayli bilgi: {WHATSAPP_LINK}"
    
    # yardim
    if any(w in p for w in ["yardim", "help", "ne yaparsin", "neler yaparsin", "ne yapabilirsin"]):
        return "Size yardimci olabilirim: /katalog (urunler), /siparis (siparis), /sikayet (sikayet). Daha fazla bilgi icin WhatsApp: {WHATSAPP_LINK}"
    
    # Tesekkur
    if any(w in p for w in ["tesekkur", "tesekkurler", "tsk", "sagol", "thank"]):
        return "Rica ederim! Yardimci olmaktan mutluluk duyarim."
    
    # Varsayilan
    return f"Boomer Brand olarak yardimci olmaktan mutluluk duyarim! Urunler: /katalog, Siparis: {WHATSAPP_LINK}"