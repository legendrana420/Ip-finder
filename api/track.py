from http.server import BaseHTTPRequestHandler
import requests
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. IP Capture - Update kiya gaya hai taaki 'X-Forwarded-For' ka pehla IP mile
        if self.headers.get('X-Forwarded-For'):
            # X-Forwarded-For mein aksar comma-separated list hoti hai, pehla IP client ka hota hai
            ip = self.headers.get('X-Forwarded-For').split(',')[0].strip()
        else:
            ip = self.client_address[0]
        
        # 2. URL Parameters se data uthana
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        token = params.get('token', [None])[0]
        chat_id = params.get('id', [None])[0]
        uid = params.get('uid', ['Unknown'])[0]
        
        # 3. Telegram par bhejna
        if token and chat_id:
            msg = f"📩 Email Opened!\n👤 ID: {uid}\n🌐 IP: {ip}"
            # URL safe encoding ka dhyan rakha gaya hai
            msg_encoded = urllib.parse.quote(msg)
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg_encoded}"
            try:
                requests.get(url, timeout=5)
            except:
                pass
        
        # 4. Transparent Pixel return
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        self.wfile.write(b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')
        return
