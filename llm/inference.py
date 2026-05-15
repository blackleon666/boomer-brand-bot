import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
from config import HF_API_KEY, WHATSAPP_LINK

# Boomer Brand system prompt
BOOMER_SYSTEM_PROMPT = """Sen Boomer Brand markasının resmi yapay zeka müşteri temsilcisin.

Kimliğin:
- Her yanıtta "Boomer Brand müşteri temsilcisi olarak" veya "Boomer Brand olarak" diye başla
- Profesyonel ama samimi bir dil kullan
- Markanın değerini ön plana çıkar
- Sorun çözücü ve güven verici ol

Yönlendirme kuralları (çok önemli):
- Fiyat, indirim, kampanya sorularında: "Detaylı bilgi ve güncel fiyatlar için WhatsApp hattımızı ziyaret edebilirsiniz: https://wa.me/boomermerter"
- Stok durumu sorularında: "Stok durumunu öğrenmek için WhatsApp'tan iletişime geçebilirsiniz: https://wa.me/boomermerter"
- Sipariş için: "Sipariş vermek için WhatsApp hattımız üzerinden size yardımcı olabiliriz: https://wa.me/boomermerter"

Sosyal medya:
- Telegram: @Boomerbrandd
- Instagram: https://www.instagram.com/boomermerter/

Kısa, öz ve Türkçe yanıtlar ver. Emoji kullanabilirsin."""

def generate(prompt, max_new_tokens=200, temperature=0.7):
    """Hugging Face Mistral API ile yanıt üretir"""
    
    # API key kontrolü
    if not HF_API_KEY or HF_API_KEY in ["YOUR_HUGGINGFACE_API_KEY_HERE", "hf_your_huggingface_token_here", ""]:
        return generate_fallback_response(prompt)
    
    try:
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        
        full_prompt = f"{BOOMER_SYSTEM_PROMPT}\n\nKullanıcı: {prompt}\n\nBoomer Brand Asistan:"
        
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
                # Temizle
                if "Boomer Brand Asistan:" in generated_text:
                    generated_text = generated_text.split("Boomer Brand Asistan:")[-1].strip()
                if "Kullanıcı:" in generated_text:
                    generated_text = generated_text.split("Kullanıcı:")[0].strip()
                return clean_response(generated_text)
            elif isinstance(output, dict) and "error" in output:
                return generate_fallback_response(prompt)
        elif response.status_code == 503:
            return generate_fallback_response(prompt)
        else:
            return generate_fallback_response(prompt)
            
    except requests.exceptions.Timeout:
        return generate_fallback_response(prompt)
    except Exception as e:
        print(f"LLM Error: {e}")
        return generate_fallback_response(prompt)

def clean_response(text):
    """Yanıtı temizle"""
    if not text:
        return "Bir şeyler ters gitti. Lütfen tekrar deneyin."
    
    # Gereksiz karakterleri temizle
    text = text.strip()
    
    # Çok uzunsa kısalt
    if len(text) > 500:
        text = text[:497] + "..."
    
    return text

def generate_fallback_response(prompt):
    """API çalışmazsa kullanılacak yedek yanıtlar"""
    prompt_lower = prompt.lower()
    
    # Selamlama
    if any(word in prompt_lower for word in ["merhaba", "selam", "hi", "hello", "hey"]):
        return "👋 Merhaba! Boomer Brand müşteri temtilcisi olarak size nasıl yardımcı olabilirim?\n\n📋 /katalog ile ürünlerimizi inceleyebilir veya sorularınızı sorabilirsiniz!"
    
    # Fiyat sorusu
    if any(word in prompt_lower for word in ["fiyat", "kaç", "ücret", "price"]):
        return "💰 Fiyatlarımız hakkında detaylı bilgi almak için WhatsApp hattımızı ziyaret edebilirsiniz:\nhttps://wa.me/boomermerter\n\nEn güncel fiyatlar ve özel teklifler için bize ulaşın!"
    
    # Ürün bilgisi
    if any(word in prompt_lower for word in ["ürün", "ürünler", "katalog", "ne var", "clothes", "giyim"]):
        return "🛍️ Ürün kataloğumuzu görmek için /katalog komutunu kullanabilirsiniz!\n\nDetaylı ürün bilgileri ve fiyatlar için WhatsApp'tan iletişime geçebilirsiniz:\nhttps://wa.me/boomermerter"
    
    # Sipariş
    if any(word in prompt_lower for word in ["sipariş", "satın", "almak", "order"]):
        return "🛒 Sipariş vermek için WhatsApp hattımız üzerinden size yardımcı olabiliriz:\nhttps://wa.me/boomermerter\n\nÜrün kataloğumuzu incelemek için /katalog komutunu kullanabilirsiniz."
    
    # Şikayet/İade
    if any(word in prompt_lower for word in ["şikayet", "iade", "sorun", " şikayet"]):
        return "📝 Şikayet veya iade talebinizi /sikayet komutuyla bize bildirebilirsiniz.\n\nAyrıca WhatsApp üzerinden de destek ekibimizle iletişime geçebilirsiniz:\nhttps://wa.me/boomermerter"
    
    # Kampanya
    if any(word in prompt_lower for word in ["kampanya", "indirim", "offer", "discount", "promo"]):
        return "🎉 Güncel kampanyalarımız ve özel indirimlerimiz hakkında bilgi almak için WhatsApp hattımızı ziyaret edebilirsiniz:\nhttps://wa.me/boomermerter\n\nAktif kampanyalarımızı kaçırmamak için Instagram ve Telegram hesaplarımızı da takip edebilirsiniz!"
    
    # İletişim
    if any(word in prompt_lower for word in ["iletişim", "contact", "ulas", "whatsapp", "telefon"]):
        return "📱 İletişim bilgilerimiz:\n\nWhatsApp: https://wa.me/boomermerter\nTelegram: @Boomerbrandd\nInstagram: https://www.instagram.com/boomermerter/"
    
    # Varsayılan yanıt
    return "🤖 Boomer Brand müşteri temsilcisi olarak size yardımcı olmaktan mutluluk duyarım!\n\n📋 Kullanabileceğiniz komutlar:\n/katalog - Ürünlerimizi görüntüle\n/siparis - Sipariş ver\n/sikayet - Şikayet bildir\n/stats - İstatistikleri görüntüle\n\nBaşka bir sorunuz varsa sormaktan çekinmeyin!"