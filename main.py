import requests
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)

        uid = query.get("uid", [None])[0]
        server_name = query.get("server_name", [None])[0]

        if not uid or not server_name:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": 0,
                "message": "uid and server_name required"
            }).encode())
            return

        api1 = f"https://semylikerrr.vercel.app/like?uid={uid}&server_name={server_name}"
        api2 = f"https://semylikes2p.vercel.app/like?uid={uid}&server_name={server_name}"

        data1 = {}
        data2 = {}

        try:
            r1 = requests.get(api1, timeout=10)
            data1 = r1.json()
        except:
            pass

        try:
            r2 = requests.get(api2, timeout=10)
            data2 = r2.json()
        except:
            pass

        likes1 = data1.get("LikesGivenByAPI", 0)
        likes2 = data2.get("LikesGivenByAPI", 0)

        before = data1.get("LikesbeforeCommand") or data2.get("LikesbeforeCommand") or 0
        after = data1.get("LikesafterCommand") or data2.get("LikesafterCommand") or 0
        nickname = data1.get("PlayerNickname") or data2.get("PlayerNickname") or "Unknown"

        total_likes = likes1 + likes2

        result = {
            "DEVELOPER": "SEMY",
            "LikesGivenByAPI": total_likes,
            "LikesafterCommand": after,
            "LikesbeforeCommand": before,
            "PlayerNickname": nickname,
            "UID": int(uid),
            "status": 1 if total_likes > 0 else 2
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
