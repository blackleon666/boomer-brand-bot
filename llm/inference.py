import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import HF_API_KEY, WHATSAPP_LINK, INSTAGRAM_LINK, TELEGRAM_GROUP_ID

BOOMER_SYSTEM_PROMPT = '''Sen "Boomer Brand" markasının resmi yapay zeka müşteri temsilcisisin.

KİMLİK:
- Her yanıtın "Boomer Brand müşteri temsilcisi olarak" veya "Boomer Brand olarak" başlamalı
- Müşteri temsilcisi, satış ve pazarlama uzmanısın
- Profesyonel, sıcak ve güven verici bir dil kullan

YÖNLENDİRME KURALLARI:
- Fiyat soruları → "Güncel fiyatlar için WhatsApp: https://wa.me/boomermerter"
- Kampanya/indirim → "Aktif kampanyalar için WhatsApp: https://wa.me/boomermerter"
- Sipariş → "Sipariş için WhatsApp: https://wa.me/boomermerter"
- Stok → "Stok için WhatsApp: https://wa.me/boomermerter"

İLETİŞİM: WhatsApp: https://wa.me/boomermerter | Instagram: https://www.instagram.com/boomermerter/ | Telegram: @Boomerbrandd'''

def generate(prompt, user_id=None, max_new_tokens=200, temperature=0.7):
    user_context = ""
    if user_id:
        try:
            from db.repo import get_user_context
            user_context = get_user_context(user_id)
        except:
            pass
    
    full_prompt = BOOMER_SYSTEM_PROMPT
    if user_context:
        full_prompt += f"\n\nKullanıcı geçmişi: {user_context}"
    full_prompt += f"\n\nKullanıcı sorusu: {prompt}\n\nAsistan:"
    
    if not HF_API_KEY or HF_API_KEY in ["YOUR_HUGGINGFACE_API_KEY_HERE", "hf_your_huggingface_token_here", ""]:
        return generate_fallback_response(prompt)
    
    try:
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "return_full_text": False,
                "top_p": 0.9
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            output = response.json()
            if isinstance(output, list) and len(output) > 0:
                generated_text = output[0].get("generated_text", "").strip()
                if "Asistan:" in generated_text:
                    generated_text = generated_text.split("Asistan:")[-1].strip()
                return clean_response(generated_text)
    except Exception as e:
        print(f"LLM Error: {e}")
    
    return generate_fallback_response(prompt)

def clean_response(text):
    if not text:
        return "Boomer Brand olarak size yardımcı olmaktan mutluluk duyarım! /katalog ile ürünlerimizi inceleyebilirsiniz."
    text = text.strip()
    if len(text) > 500:
        text = text[:497] + "..."
    return text

def generate_fallback_response(prompt):
    prompt_lower = prompt.lower()
    
    if any(w in prompt_lower for w in ["merhaba", "selam", "hi", "naber"]):
        return "👋 Merhaba! Boomer Brand müşteri temsilcisi olarak size nasıl yardımcı olabilirim? /katalog ile ürünlerimizi inceleyebilirsiniz!"
    
    if any(w in prompt_lower for w in ["fiyat", "kaç", "ücret", "ne kadar"]):
        return "💰 Güncel fiyatlar ve özel teklifler için WhatsApp hattımızı ziyaret edebilirsiniz:\nhttps://wa.me/boomermerter"
    
    if any(w in prompt_lower for w in ["kampanya", "indirim", "promo"]):
        return "🎉 Aktif kampanyalar ve özel indirimler için WhatsApp hattımız:\nhttps://wa.me/boomermerter"
    
    if any(w in prompt_lower for w in ["sipariş", "satın", "almak"]):
        return "🛒 Sipariş vermek için hemen WhatsApp hattımızdan size yardımcı olabiliriz:\nhttps://wa.me/boomermerter"
    
    if any(w in prompt_lower for w in ["şikayet", "iade", "sorun"]):
        return "📝 Şikayetinizi /sikayet komutuyla bildirebilir veya WhatsApp üzerinden destek ekibimizle iletişime geçebilirsiniz:\nhttps://wa.me/boomermerter"
    
    if any(w in prompt_lower for w in ["ürün", "katalog", "ne var"]):
        return "🛍️ Ürünlerimizi görmek için /katalog komutunu kullanabilirsiniz! Detaylar için WhatsApp: https://wa.me/boomermerter"
    
    return "🤖 Boomer Brand olarak size yardımcı olmaktan mutluluk duyarım!\n\n/katalog - Ürünler\n/siparis - Sipariş\n/sikayet - Şikayet\n\nBaşka sorunuz varsa sorun!"