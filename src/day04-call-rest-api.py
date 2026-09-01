import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("API_KEY")
api_llm_url = os.getenv("API_LLM_URL")

payload = {
    "model": "qwen3.5:4b-mlx",
    "prompt": "สวัสดี แนะนำตัวเองสั้นๆ หน่อย",
    "stream": False
}

print("Calling Ollama...")
print("URL:", api_llm_url)
print("Model:", payload["model"])

headers = {
    "Authorization": f"Bearer {api_key}",
}

response = requests.post(
    url=api_llm_url, 
    json=payload, 
    headers=headers,
    timeout=300.0
)

print("HTTP Status:", response.status_code)

if response.status_code == 401:
    print("API key ไม่ถูกต้องหรือหมดอายุ — แก้ key ก่อน retry ไม่มีประโยชน์")
elif response.status_code == 429:
    print("โดน rate limit — ควรรอสักพักแล้วค่อย retry")
elif response.status_code >= 500:
    print("ปัญหาฝั่งเซิร์ฟเวอร์ — retry ได้ มักหายเองใน 2-3 ครั้ง")

response.raise_for_status()

ollama_result = response.json()

result = {
    "answer": ollama_result["response"],
    "model": ollama_result["model"],
    "usage": {
        "prompt_tokens": ollama_result.get("prompt_eval_count", 0),
        "completion_tokens": ollama_result.get("eval_count", 0),
        "total_duration": ollama_result.get("total_duration", 0)
    }
}

print(result)

# {'answer': 'สวัสดีครับ! ผมเป็น AI ผู้ช่วยที่พร้อมช่วยเหลือคุณเสมอ ไม่ว่าจะเป็นการตอบคำถาม ช่วยวิเคราะห์ข้อมูล เขียนโค้ด หรือช่วยสร้างเนื้อหาอื่นๆ แค่บอกมาได้เลยนะครับ ยินดีที่ได้รู้จัก! 😊', 'model': 'qwen3.5:4b-mlx', 'usage': {'prompt_tokens': 18, 'completion_tokens': 1532, 'total_duration': 44544835625}}