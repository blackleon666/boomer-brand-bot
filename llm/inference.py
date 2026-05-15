import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import HF_API_KEY

# Boomer Brand system prompt - Marka temsilcisi olarak davran
BOOMER_SYSTEM_PROMPT = """Sen Boomer Brand markasının resmi yapay zeka müşteri temsilcisin. Aynı zamanda bir Müşteri Sorumlusu ve Pazarlama Şefi yetkinliklerine sahipsin.

Özellikler:
- Her zaman Boomer Brand müşteri temsilcisi olarak kendini tanıt
- Profesyonel ama samimi bir dil kullan
- Markanın değerini ön plana çıkar
- Sorun çözücü ve güven verici ol
- Müşterilere tarz, kombin veya ürün kullanımı hakkında içerik odaklı tavsiyeler sun

Yönlendirme Kuralları:
- Fiyat bilgisi, indirim veya kampanya sorularında WhatsApp'a yönlendir: https://wa.me/boomermerter
- Detaylı bilgi için her zaman WhatsApp'ı öner

Kısa ve öz yanıtlar ver. Türkçe konuş."""

def query_huggingface(prompt, max_new_tokens=150, temperature=0.7):
    """Hugging Face Inference API kullanarak yanıt üretir"""
    if not HF_API_KEY or HF_API_KEY == "YOUR_HUGGINGFACE_API_KEY_HERE":
        return "Üzgünüm, yapay zeka servisi şu anda aktif değil. Detaylı bilgi için WhatsApp'tan iletişime geçebilirsiniz: https://wa.me/boomermerter"
    
    try:
        # Mistral modelini kullan (ücretsiz ve iyi performans)
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        
        full_prompt = f"{BOOMER_SYSTEM_PROMPT}\n\nKullanıcı: {prompt}\nBoomer Brand Asistan:"
        
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "return_full_text": False,
                "top_p": 0.9,
                "do_sample": True
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            output = response.json()
            if isinstance(output, list) and len(output) > 0:
                generated_text = output[0].get("generated_text", "").strip()
                # Yanıtı temizle
                if "Boomer Brand Asistan:" in generated_text:
                    generated_text = generated_text.split("Boomer Brand Asistan:")[-1].strip()
                return generated_text if generated_text else "Bir şeyler ters gitti. Lütfen tekrar deneyin."
            elif isinstance(output, dict) and "error" in output:
                return f"Servis şu anda meşgul. Detaylı bilgi için: https://wa.me/boomermerter"
        else:
            return "Bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            
    except Exception as e:
        print(f"LLM Error: {e}")
        return "Şu anda yanıt üretemiyorum. Detaylı bilgi için WhatsApp'tan iletişime geçebilirsiniz: https://wa.me/boomermerter"

def generate(prompt, max_new_tokens=150, temperature=0.7):
    """Kısayol fonksiyon"""
    return query_huggingface(prompt, max_new_tokens, temperature)