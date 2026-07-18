from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import base64

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. IP Capture
        if self.headers.get('X-Forwarded-For'):
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
            msg_encoded = urllib.parse.quote(msg)
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg_encoded}"
            
            try:
                # 'requests' ki jagah built-in module use kiya hai taaki Vercel par error na aaye
                req = urllib.request.Request(url)
                urllib.request.urlopen(req, timeout=5)
                print(f"Success: Message sent for {uid}")
            except Exception as e:
                # Agar fail hoga toh Vercel logs mein error dikhega, silent nahi rahega
                print(f"Error sending to Telegram: {e}")
        
        # 4. Transparent Pixel return (Sahi Base64 decoding ke sath)
        pixel_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        pixel_data = base64.b64decode(pixel_b64)
        
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(pixel_data)
        return
