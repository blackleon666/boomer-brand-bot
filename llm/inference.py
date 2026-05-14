import os
import requests
import json

HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate(prompt, max_new_tokens=150, temperature=0.7):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "return_full_text": False
        }
    }
    output = query_huggingface(payload)
    if isinstance(output, list) and len(output) > 0:
        return output[0].get("generated_text", "").strip()
    elif isinstance(output, dict) and "error" in output:
        # Handle error (e.g., model loading)
        return f"Üzgünüm, şu anda yanıt üretemiyorum. Lütfen daha sonra tekrar deneyin."
    else:
        return "Bir şeyler ters gitti. Lütfen daha sonra tekrar deneyin."
