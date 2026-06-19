import os
import requests
import urllib.parse
from http.server import BaseHTTPRequestHandler
import json

TOKEN = os.environ.get("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}/"

def send_msg(chat_id, text):
    try: requests.post(API_URL + "sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except: pass

def send_photo(chat_id, photo_url, caption):
    try: requests.post(API_URL + "sendPhoto", json={"chat_id": chat_id, "photo": photo_url, "caption": caption}, timeout=20)
    except: pass

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            up = json.loads(post_data.decode('utf-8'))
            if "message" in up and "text" in up["message"]:
                cid = up["message"]["chat"]["id"]
                txt = up["message"]["text"]
                
                if txt == "/start":
                    send_msg(cid, "🚀 Бот успешно запущен на сверхбыстром Vercel!\n\nНапиши мне тему для фото на русском, и я моментально сгенерирую её во Flux 4K!")
                else:
                    send_msg(cid, "🔄 Начинаю моментальную генерацию во Flux...")
                    
                    try:
                        tr = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={urllib.parse.quote(txt)}", timeout=5).json()
                        eng_text = tr[0][0][0]
                    except:
                        eng_text = txt

                    prompt = f"{eng_text}, high-quality photo, photorealistic, 4k, realistic skin texture, visible pores, grain, natural cinematic lighting, aesthetic, candid shot, dslr"
                    encoded_prompt = urllib.parse.quote(prompt)
                    img_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1080&height=1350&enhanced=true&seed=77"
                    
                    send_photo(cid, img_url, f"✨ Готово!\n📸 Промпт: {txt}")
        except Exception as e:
            pass

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
        return
      
