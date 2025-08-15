import discord
from discord.ext import commands
import threading
import time
import re
import requests
import os
import random
import asyncio
import datetime
import json
import base64
import aiohttp
import traceback
import shutil
import hashlib
from typing import Dict, Any
from threading import Thread

os.system("clear")

print("""
░█████╗░███████╗░██████╗██╗░░██╗
██╔══██╗██╔════╝██╔════╝██║░░██║
███████║█████╗░░╚█████╗░███████║
██╔══██║██╔══╝░░░╚═══██╗██╔══██║
██║░░██║███████╗██████╔╝██║░░██║
╚═╝░░╚═╝╚══════╝╚═════╝░╚═╝░░╚═╝
ADMIN NG QUANG HUY X BOT""")
TOKEN = input("\033[34m [NG QUANG HUY BOT]\033[35m Vui lòng nhập token bot:\033[37m")
NG_QUANG_HUY_ID = int(input("\033[34m [NG QUANG HUY BOT]\033[35m Vui lòng nhập id admin:\033[37m "))
ng_quang_huy_list = []
IDNG_QUANG_HUY_GOC = NG_QUANG_HUY_ID

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def ngquanghuy_dzi_on_ready():
    print(f"\033[35m》{bot.user}《 đã bật chế độ hotwar 2025!")

allowed_users = set()
treo_threads = {}
treo_start_times = {}
messenger_instances = {}
nhay_threads = {}
nhay_start_times = {}
chui_threads = {}
chui_start_times = {}
codelag_threads = {}
codelag_start_times = {}
so_threads = {}
so_start_times = {}
running_tasks = {}
task_info = {}
start_time = datetime.datetime.utcnow()

UA_KIWI = [
    "Mozilla/5.0 (Linux; Android 11; RMX2185) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.129 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.68 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; V2031) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.60 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; CPH2481) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Mobile Safari/537.36"
]

UA_VIA = [
    "Mozilla/5.0 (Linux; Android 10; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.0.0 Mobile Safari/537.36 Via/4.8.2",
    "Mozilla/5.0 (Linux; Android 11; V2109) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.138 Mobile Safari/537.36 Via/4.9.0",
    "Mozilla/5.0 (Linux; Android 13; TECNO POVA 5) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.134 Mobile Safari/537.36 Via/5.0.1",
    "Mozilla/5.0 (Linux; Android 12; Infinix X6710) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.138 Mobile Safari/537.36 Via/5.2.0",
    "Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.112 Mobile Safari/537.36 Via/5.3.1"
]

USER_AGENTS = UA_KIWI + UA_VIA

class Messenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.ngquanghuy_dzi_id_user()
        self.user_agent = random.choice(USER_AGENTS)
        self.fb_dtsg = None
        self.ngquanghuy_dzi_init_params()

    def ngquanghuy_dzi_id_user(self):
        try:
            c_user = re.search(r"c_user=(\d+)", self.cookie).group(1)
            return c_user
        except:
            raise Exception("Cookie không hợp lệ")

    def ngquanghuy_dzi_init_params(self):
        headers = {
            "Cookie": self.cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }

        try:
            response = requests.get("https://www.facebook.com", headers=headers)
            fb_dtsg_match = re.search(r'"token":"(.*?)"', response.text)

            if not fb_dtsg_match:
                response = requests.get("https://mbasic.facebook.com", headers=headers)
                fb_dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)

                if not fb_dtsg_match:
                    response = requests.get("https://m.facebook.com", headers=headers)
                    fb_dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)

            if fb_dtsg_match:
                self.fb_dtsg = fb_dtsg_match.group(1)
            else:
                raise Exception("Không thể lấy được fb_dtsg")

        except Exception as e:
            raise Exception(f"Lỗi khi khởi tạo tham số: {str(e)}")

    def ngquanghuy_dzi_gui_tn(self, recipient_id, message, max_retries=10):
        for attempt in range(max_retries):
            timestamp = int(time.time() * 1000)
            offline_threading_id = str(timestamp)
            message_id = str(timestamp)

            data = {
                "thread_fbid": recipient_id,
                "action_type": "ma-type:user-generated-message",
                "body": message,
                "client": "mercury",
                "author": f"fbid:{self.user_id}",
                "timestamp": timestamp,
                "source": "source:chat:web",
                "offline_threading_id": offline_threading_id,
                "message_id": message_id,
                "ephemeral_ttl_mode": "",
                "__user": self.user_id,
                "__a": "1",
                "__req": "1b",
                "__rev": "1015919737",
                "fb_dtsg": self.fb_dtsg
            }

            headers = {
                "Cookie": self.cookie,
                "User-Agent": self.user_agent,
                "Accept": "*/*",
                "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://www.facebook.com",
                "Referer": f"https://www.facebook.com/messages/t/{recipient_id}",
                "Host": "www.facebook.com",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty"
            }

            try:
                response = requests.post(
                    "https://www.facebook.com/messaging/send/",
                    data=data,
                    headers=headers
                )
                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": "HTTP_ERROR",
                        "error_description": f"Status code: {response.status_code}"
                    }

                if "for (;;);" in response.text:
                    clean_text = response.text.replace("for (;;);", "")
                    try:
                        result = json.loads(clean_text)
                        if "error" in result:
                            return {
                                "success": False,
                                "error": result.get("error"),
                                "error_description": result.get("errorDescription", "Unknown error")
                            }
                        return {
                            "success": True,
                            "message_id": message_id,
                            "timestamp": timestamp
                        }
                    except json.JSONDecodeError:
                        pass

                return {
                    "success": True,
                    "message_id": message_id,
                    "timestamp": timestamp
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": "REQUEST_ERROR",
                    "error_description": str(e)
                }

def ngquanghuy_dzi_format_duration(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    parts = []
    if d: parts.append(f"{d} ngày")
    if h: parts.append(f"{h} giờ")
    if m: parts.append(f"{m} phút")
    if s or not parts: parts.append(f"{s} giây")
    return " ".join(parts)

def ngquanghuy_dzi_start_spam(user_id, idbox, cookie, message, delay):
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    def loop_send():
        while (user_id, idbox) in treo_threads:
            success = messenger.ngquanghuy_dzi_gui_tn(idbox, message)
            print(f"Gửi Tin Nhắn {'Thành Công' if success['success'] else 'Thất Bại'}")
            time.sleep(delay)

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_send)
    treo_threads[key] = thread
    treo_start_times[key] = time.time()
    messenger_instances[key] = messenger
    thread.start()
    return "Đã bắt đầu gửi tin nhắn."

def ngquanghuy_dzi_start_nhay(user_id, idbox, cookie, delay):
    if not os.path.exists("nhay.txt"):
        return "Không tìm thấy file nhay.txt."
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    with open("nhay.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return "File nhay.txt không có nội dung."

    def loop_nhay():
        index = 0
        while (user_id, idbox) in nhay_threads:
            message = messages[index % len(messages)]
            success = messenger.ngquanghuy_dzi_gui_tn(idbox, message)
            print(f"Gửi tin nhắn {'Thành công' if success['success'] else 'Thất bại'}")
            time.sleep(delay)
            index += 1

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_nhay)
    nhay_threads[key] = thread
    nhay_start_times[key] = time.time()
    thread.start()
    return "Đã bắt đầu nhây."

def ngquanghuy_dzi_start_chui(user_id, idbox, cookie, delay):
    if not os.path.exists("chui.txt"):
        return "Không tìm thấy file chui.txt."
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    with open("chui.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return "File chui.txt không có nội dung."

    def loop_chui():
        index = 0
        while (user_id, idbox) in chui_threads:
            message = messages[index % len(messages)]
            success = messenger.ngquanghuy_dzi_gui_tn(idbox, message)
            print(f"Gửi tin nhắn {'Thành công' if success['success'] else 'Thất bại'}")
            time.sleep(delay)
            index += 1

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_chui)
    chui_threads[key] = thread
    chui_start_times[key] = time.time()
    thread.start()
    return "Đã bắt đầu gửi tin nhắn."

def ngquanghuy_dzi_start_codelag(user_id, idbox, cookie, delay):
    if not os.path.exists("codelag.txt"):
        return "Không tìm thấy file codelag.txt."
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    with open("codelag.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return "File codelag.txt không có nội dung."

    def loop_codelag():
        index = 0
        while (user_id, idbox) in codelag_threads:
            message = messages[index % len(messages)]
            success = messenger.ngquanghuy_dzi_gui_tn(idbox, message)
            print(f"Gửi tin nhắn {'Thành công' if success['success'] else 'Thất bại'}")
            time.sleep(delay)
            index += 1

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_codelag)
    codelag_threads[key] = thread
    codelag_start_times[key] = time.time()
    thread.start()
    return "Đã bắt đầu spam code lag."

def ngquanghuy_dzi_start_so(user_id, idbox, cookie, delay):
    if not os.path.exists("so.txt"):
        return "Không tìm thấy file so.txt."
    try:
        messenger = Messenger(cookie)
    except Exception as e:
        return f"Lỗi cookie: {str(e)}"

    with open("so.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return "File so.txt không có nội dung."

    def loop_so():
        index = 0
        while (user_id, idbox) in so_threads:
            message = messages[index % len(messages)]
            success = messenger.ngquanghuy_dzi_gui_tn(idbox, message)
            print(f"Gửi tin nhắn {'Thành công' if success['success'] else 'Thất bại'}")
            time.sleep(delay)
            index += 1

    key = (user_id, idbox)
    thread = threading.Thread(target=loop_so)
    so_threads[key] = thread
    so_start_times[key] = time.time()
    thread.start()
    return "Đã bắt đầu gửi tin nhắn."

def ngquanghuy_dzi_get_guid():
    section_length = int(time.time() * 1000)
    
    def replace_func(c):
        nonlocal section_length
        r = (section_length + random.randint(0, 15)) % 16
        section_length //= 16
        return hex(r if c == "x" else (r & 7) | 8)[2:]

    return "".join(replace_func(c) if c in "xy" else c for c in "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx")

def ngquanghuy_dzi_normalize_cookie(cookie, domain="www.facebook.com"):
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(f"https://{domain}/", headers=headers, timeout=10)
        if response.status_code == 200:
            set_cookie = response.headers.get("Set-Cookie", "")
            new_tokens = re.findall(r"([a-zA-Z0-9_-]+)=[^;]+", set_cookie)
            cookie_dict = dict(re.findall(r"([a-zA-Z0-9_-]+)=([^;]+)", cookie))
            for token in new_tokens:
                if token not in cookie_dict:
                    cookie_dict[token] = ""
            return ";".join(f"{k}={v}" for k, v in cookie_dict.items() if v)
    except:
        pass
    return cookie

def ngquanghuy_dzi_get_uid_fbdtsg(ck):
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
            "Connection": "keep-alive",
            "Cookie": ck,
            "Host": "www.facebook.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        
        try:
            response = requests.get("https://www.facebook.com/", headers=headers)
            
            if response.status_code != 200:
                print(f"Status Code >> {response.status_code}")
                return None, None, None, None, None, None
                
            html_content = response.text
            
            user_id = None
            fb_dtsg = None
            jazoest = None
            
            script_tags = re.findall(r'<script id="__eqmc" type="application/json[^>]*>(.*?)</script>', html_content)
            for script in script_tags:
                try:
                    json_data = json.loads(script)
                    if "u" in json_data:
                        user_param = re.search(r'__user=(\d+)', json_data["u"])
                        if user_param:
                            user_id = user_param.group(1)
                            break
                except:
                    continue
            
            fb_dtsg_match = re.search(r'"f":"([^"]+)"', html_content)
            if fb_dtsg_match:
                fb_dtsg = fb_dtsg_match.group(1)
            
            jazoest_match = re.search(r'jazoest=(\d+)', html_content)
            if jazoest_match:
                jazoest = jazoest_match.group(1)
            
            revision_match = re.search(r'"server_revision":(\d+),"client_revision":(\d+)', html_content)
            rev = revision_match.group(1) if revision_match else ""
            
            a_match = re.search(r'__a=(\d+)', html_content)
            a = a_match.group(1) if a_match else "1"
            
            req = "1b"
                
            return user_id, fb_dtsg, rev, req, a, jazoest
                
        except requests.exceptions.RequestException as e:
            print(f"Lỗi Kết Nối Khi Lấy UID/FB_DTSG: {e}")
            return ngquanghuy_dzi_get_uid_fbdtsg(ck)
            
    except Exception as e:
        print(f"Lỗi: {e}")
        return None, None, None, None, None, None
class CommandModal(discord.ui.Modal):
    def __init__(self, command_name, fields, callback):
        super().__init__(title=f"Nhập thông tin cho lệnh {command_name}", timeout=300)
        self.command_name = command_name
        self.callback = callback
        for label, placeholder in fields:
            self.add_item(discord.ui.TextInput(
                label=label,
                placeholder=placeholder,
                required=True
            ))

    async def on_submit(self, interaction: discord.Interaction):
        await self.callback(interaction, *[item.value for item in self.children])

class NgQuangHuyMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.current_page = 0
        self.per_page = 5
        self.commands = [
            ("menu", "Xem các chức năng của bot", []),
            ("uptime", "Xem thời gian bot hoạt động", []),
            ("ping", "Kiểm tra độ trễ của bot", []),
            ("idkenh", "Lấy ID kênh", []),
            ("idsv", "Lấy ID máy chủ", []),
            ("video", "Treo video ngẫu nhiên", []),
            ("ngonmess", "Treo ngôn Messenger", [
                ("ID Box", "Nhập ID box Messenger"),
                ("Cookie", "Nhập cookie tài khoản Facebook"),
                ("Tên File", "Nhập tên file .txt đã set"),
                ("Delay", "Nhập thời gian delay (giây)")
            ]),
            ("nhaymess", "Nhây Messenger", [
                ("ID Box", "Nhập ID box Messenger"),
                ("Cookie", "Nhập cookie tài khoản Facebook"),
                ("Delay", "Nhập thời gian delay (giây)")
            ]),
            ("ideamess", "Chửi idea Messenger", [
                ("ID Box", "Nhập ID box Messenger"),
                ("Cookie", "Nhập cookie tài khoản Facebook"),
                ("Delay", "Nhập thời gian delay (giây)")
            ]),
            ("so", "Treo sớ Messenger", [
                ("ID Box", "Nhập ID box Messenger"),
                ("Cookie", "Nhập cookie tài khoản Facebook"),
                ("Delay", "Nhập thời gian delay (giây)")
            ]),
            ("codelag", "Nhây + code lag Messenger", [
                ("ID Box", "Nhập ID box Messenger"),
                ("Cookie", "Nhập cookie tài khoản Facebook"),
                ("Delay", "Nhập thời gian delay (giây)")
            ]),
            ("stop", "Dừng lệnh war đang chạy", [
                ("Lệnh", "Nhập lệnh (ngonmess, nhaymess, ideamess, so, codelag)"),
                ("ID Box", "Nhập ID box Messenger")
            ]),
            ("setngonmess", "Set file ngôn cho treo Messenger", []),
            ("addadmin", "Thêm người dùng làm admin", [
                ("User ID", "Nhập ID người dùng Discord")
            ]),
            ("xoaadmin", "Xoá admin", [
                ("User ID", "Nhập ID người dùng Discord")
            ]),
            ("tab", "Xem các task đang chạy", [
                ("Lệnh", "Nhập lệnh (ngonmess, nhaymess, ideamess, so, codelag)")
            ]),
            ("spam", "Spam nội dung Discord", [
                ("Channel IDs", "Nhập danh sách ID kênh, cách nhau bằng dấu phẩy"),
                ("Delay", "Nhập thời gian delay (giây)"),
                ("Nội dung", "Nhập nội dung để spam")
            ]),
            ("nhay", "Nhây Discord nhiều kênh", [
                ("Channel IDs", "Nhập danh sách ID kênh, cách nhau bằng dấu phẩy"),
                ("Delay", "Nhập thời gian delay (giây)")
            ]),
            ("stopspam", "Dừng tất cả task spam Discord", []),
            ("stopnhay", "Dừng task nhây Discord", [
                ("Channel ID", "Nhập ID kênh hoặc để trống để dừng tất cả")
            ])
        ]
        self.pages = self.ngquanghuy_dzi_build_pages()

    def ngquanghuy_dzi_build_pages(self):
        pages = []
        titles = [
            "🛠 Tiện Ích Discord",
            "📨 Chức Năng Messenger",
            "🌐 Chức Năng Messenger 2"
        ]
        
        for i in range(0, len(self.commands), self.per_page):
            chunk = self.commands[i:i+self.per_page]
            page_number = len(pages) + 1
            embed = discord.Embed(
                title=titles[page_number - 1] if page_number <= len(titles) else "Trang Khác",
                description="Chọn nút bên dưới để thực thi lệnh.",
                color=discord.Color.from_rgb(106, 13, 173)
            )
            embed.set_thumbnail(url="https://files.catbox.moe/u4b8wz.jpg")
            embed.set_footer(text=f"Trang {page_number}/{(len(self.commands)-1)//self.per_page + 1} | Bot by Ng Quang Huy")
            for cmd, desc, _ in chunk:
                embed.add_field(name=f"🔹 {cmd}", value=desc, inline=False)
            pages.append(embed)
        
        return pages

    async def ngquanghuy_dzi_add_buttons(self):
        self.clear_items()
        start_idx = self.current_page * self.per_page
        for i, (cmd, desc, fields) in enumerate(self.commands[start_idx:start_idx + self.per_page]):
            button = discord.ui.Button(
                label=cmd,
                style=discord.ButtonStyle.primary,
                custom_id=f"cmd_{cmd}_{i}"
            )
            async def button_callback(interaction: discord.Interaction, cmd=cmd, fields=fields):
                if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC and cmd not in ["menu", "uptime", "ping"]:
                    embed = discord.Embed(
                        title="🚫 Lỗi Quyền Hạn",
                        description="Bạn không có quyền sử dụng lệnh này.",
                        color=discord.Color.from_rgb(255, 0, 0)
                    )
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                if not fields:
                    await getattr(self, f"execute_{cmd}")(interaction)
                else:
                    modal = CommandModal(cmd, fields, getattr(self, f"execute_{cmd}"))
                    await interaction.response.send_modal(modal)
            button.callback = button_callback
            self.add_item(button)

        if self.current_page > 0:
            prev_button = discord.ui.Button(label="⬅ Trước", style=discord.ButtonStyle.secondary, custom_id="prev_button")
            prev_button.callback = self.ngquanghuy_dzi_previous
            self.add_item(prev_button)

        if self.current_page < len(self.pages) - 1:
            next_button = discord.ui.Button(label="Tiếp ➡️", style=discord.ButtonStyle.secondary, custom_id="next_button")
            next_button.callback = self.ngquanghuy_dzi_next
            self.add_item(next_button)

    async def ngquanghuy_dzi_previous(self, interaction: discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await self.ngquanghuy_dzi_update(interaction)

    async def ngquanghuy_dzi_next(self, interaction: discord.Interaction):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.ngquanghuy_dzi_update(interaction)

    async def ngquanghuy_dzi_update(self, interaction: discord.Interaction):
        await self.ngquanghuy_dzi_add_buttons()
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    async def execute_menu(self, interaction: discord.Interaction):
        await self.ngquanghuy_dzi_update(interaction)

    async def execute_uptime(self, interaction: discord.Interaction):
        now = datetime.datetime.utcnow()
        delta = now - start_time
        total_seconds = int(delta.total_seconds())
        seconds = total_seconds % 60
        minutes = (total_seconds // 60) % 60
        hours = (total_seconds // 3600) % 24
        days = (total_seconds // 86400) % 7
        weeks = (total_seconds // 604800) % 4
        months = (total_seconds // 2592000) % 12  
        years = total_seconds // 31536000
        embed = discord.Embed(
            title="⏰ Thời Gian Hoạt Động",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        embed.add_field(name="Thời gian hoạt động", value='\n'.join([
            f"> `{years}` năm",
            f"> `{months}` tháng",
            f"> `{weeks}` tuần",
            f"> `{days}` ngày",
            f"> `{hours}` giờ",
            f"> `{minutes}` phút",
            f"> `{seconds}` giây",
        ]), inline=False)
        embed.set_footer(text=f"Yêu cầu bởi {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_ping(self, interaction: discord.Interaction):
        latency = bot.latency * 1000
        embed = discord.Embed(
            title="🏓 Độ Trễ Bot",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        embed.add_field(name="Độ trễ hiện tại", value=f"> `{latency:.2f} ms`", inline=False)
        embed.set_footer(text=f"Yêu cầu bởi {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_idkenh(self, interaction: discord.Interaction):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng lệnh này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(
            title="🆔 ID Kênh",
            description=f"Channel ID: {interaction.channel.id}",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_idsv(self, interaction: discord.Interaction):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng lệnh này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(
            title="🆔 ID Server",
            description=f"Server ID: {interaction.guild.id}",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_video(self, interaction: discord.Interaction):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        if not os.path.exists("video.txt"):
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="Không tìm thấy file video.txt.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        with open("videol.txt", "r", encoding="utf-8") as f:
            videos = [line.strip() for line in f if line.strip()]
        
        if not videos:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="File video.txt không có nội dung.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        video_url = random.choice(videos)
        embed = discord.Embed(
            title="🎥 Video Ngẫu Nhiên",
            description="Dưới đây là một video ngẫu nhiên từ file video.txt!",
            color=discord.Color.from_rgb(106, 13, 173)
        )
        embed.add_field(name="Link Video", value=video_url, inline=False)
        embed.set_footer(text=f"Yêu cầu bởi {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_ngonmess(self, interaction: discord.Interaction, idbox: str, cookie: str, filename: str, delay: str):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        filepath = f"{interaction.user.id}_{filename}"
        if not os.path.exists(filepath):
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="Không tìm thấy file đã set.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        with open(filepath, "r", encoding="utf-8") as f:
            message = f.read()
        result = ngquanghuy_dzi_start_spam(interaction.user.id, idbox, cookie, message, int(delay))
        embed = discord.Embed(
            title="✅ Thành Công",
            description=result,
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_nhaymess(self, interaction: discord.Interaction, idbox: str, cookie: str, delay: str):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        result = ngquanghuy_dzi_start_nhay(interaction.user.id, idbox, cookie, int(delay))
        embed = discord.Embed(
            title="✅ Thành Công",
            description=result,
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_ideamess(self, interaction: discord.Interaction, idbox: str, cookie: str, delay: str):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        result = ngquanghuy_dzi_start_chui(interaction.user.id, idbox, cookie, int(delay))
        embed = discord.Embed(
            title="✅ Thành Công",
            description=result,
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_so(self, interaction: discord.Interaction, idbox: str, cookie: str, delay: str):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        result = ngquanghuy_dzi_start_so(interaction.user.id, idbox, cookie, int(delay))
        embed = discord.Embed(
            title="✅ Thành Công",
            description=result,
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_codelag(self, interaction: discord.Interaction, idbox: str, cookie: str, delay: str):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        result = ngquanghuy_dzi_start_codelag(interaction.user.id, idbox, cookie, int(delay))
        embed = discord.Embed(
            title="✅ Thành Công",
            description=result,
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_stop(self, interaction: discord.Interaction, command: str, idbox: str):
        commands = {
            "ngonmess": ngquanghuy_dzi_stopngonmess,
            "nhaymess": ngquanghuy_dzi_stopnhaymess,
            "ideamess": ngquanghuy_dzi_stopideamess,
            "so": ngquanghuy_dzi_stopso,
            "codelag": ngquanghuy_dzi_stopcodelag
        }
        if command not in commands:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="Lệnh không hợp lệ. Vui lòng chọn: ngonmess, nhaymess, ideamess, so, codelag.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await commands[command](interaction, idbox)

    async def execute_setngonmess(self, interaction: discord.Interaction):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(
            title="📤 Set Ngôn Messenger",
            description="Vui lòng gửi file .txt trong kênh này.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.attachments
        try:
            msg = await bot.wait_for("message", timeout=60.0, check=check)
            attachment = msg.attachments[0]
            if not attachment.filename.endswith(".txt"):
                embed = discord.Embed(
                    title="⚠️ Lỗi Định Dạng",
                    description="Bot chỉ chấp nhận file .txt.",
                    color=discord.Color.from_rgb(255, 0, 0)
                )
                return await interaction.followup.send(embed=embed, ephemeral=True)
            path = f"{interaction.user.id}_{attachment.filename}"
            await attachment.save(path)
            embed = discord.Embed(
                title="✅ Thành Công",
                description=f"Đã lưu file thành công dưới tên: `{path}`.",
                color=discord.Color.from_rgb(0, 102, 204)
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="⚠️ Hết Thời Gian",
                description="Hết thời gian chờ file .txt.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    async def execute_addadmin(self, interaction: discord.Interaction, user_id: str):
        if interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng lệnh này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        try:
            member = await bot.fetch_user(int(user_id))
            if member.id not in ng_quang_huy_list:
                ng_quang_huy_list.append(member.id)
                embed = discord.Embed(
                    title="✅ Thành Công",
                    description=f"Đã thêm `{member.name}` vào danh sách ng quang huy.",
                    color=discord.Color.from_rgb(0, 102, 204)
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Lỗi",
                    description="Người này đã là ng quang huy rồi.",
                    color=discord.Color.from_rgb(255, 0, 0)
                )
        except:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="ID người dùng không hợp lệ.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_xoaadmin(self, interaction: discord.Interaction, user_id: str):
        if interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng lệnh này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        try:
            member = await bot.fetch_user(int(user_id))
            if member.id in ng_quang_huy_list and member.id != IDNG_QUANG_HUY_GOC:
                ng_quang_huy_list.remove(member.id)
                to_remove = [task_id for task_id, info in task_info.items() if info["ng_quang_huy_id"] == member.id]
                for task_id in to_remove:
                    if task_id in running_tasks:
                        running_tasks[task_id].cancel()
                        del running_tasks[task_id]
                    del task_info[task_id]
                embed = discord.Embed(
                    title="✅ Thành Công",
                    description=f"Đã xoá `{member.name}` khỏi danh sách ng quang huy.\nĐã dừng tất cả các task do `{member.name}` tạo.",
                    color=discord.Color.from_rgb(0, 102, 204)
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Lỗi",
                    description="Không thể xoá ng quang huy gốc hoặc người này không phải ng quang huy.",
                    color=discord.Color.from_rgb(255, 0, 0)
                )
        except:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="ID người dùng không hợp lệ.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_tab(self, interaction: discord.Interaction, command: str):
        commands = {
            "ngonmess": (treo_start_times, "Danh Sách Tab Treo"),
            "nhaymess": (nhay_start_times, "Danh Sách Tab Nhây"),
            "ideamess": (chui_start_times, "Danh Sách Tab Chửi"),
            "so": (so_start_times, "Danh Sách Tab Sớ"),
            "codelag": (codelag_start_times, "Danh Sách Tab Code Lag")
        }
        if command not in commands:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="Lệnh không hợp lệ. Vui lòng chọn: ngonmess, nhaymess, ideamess, so, codelag.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        start_times, title = commands[command]
        msg = f"**{title}**\n\n"
        count = 0
        for (uid, ib), start in start_times.items():
            if uid == interaction.user.id:
                uptime = ngquanghuy_dzi_format_duration(time.time() - start)
                msg += f"**{ib}:** {uptime}\n"
                count += 1
        if count == 0:
            msg = f"**[NG QUANG HUY BOT]** Bạn không có tab {command} nào đang chạy."
        embed = discord.Embed(
            title=f"📋 {title}",
            description=msg,
            color=discord.Color.from_rgb(106, 13, 173)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_spam(self, interaction: discord.Interaction, channel_ids: str, delay: str, content: str):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        channel_ids_list = [int(id.strip()) for id in channel_ids.split(",")]

        async def spam_channel(channel_id):
            try:
                channel = bot.get_channel(channel_id)
                if channel:
                    while True:
                        await channel.send(content)
                        await asyncio.sleep(int(delay))
            except Exception as e:
                print(f"Lỗi khi spam kênh {channel_id}: {e}")

        spamming_tasks = []
        for cid in channel_ids_list:
            task = bot.loop.create_task(spam_channel(cid))
            spamming_tasks.append(task)

        embed = discord.Embed(
            title="✅ Thành Công",
            description="Đã bắt đầu spam.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_stopspam(self, interaction: discord.Interaction):
        if interaction.user.id not in ng_quang_huy_list and interaction.user.id != IDNG_QUANG_HUY_GOC:
            embed = discord.Embed(
                title="🚫 Lỗi Quyền Hạn",
                description="Bạn không có quyền sử dụng bot này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        for task in spamming_tasks:
            task.cancel()
        spamming_tasks.clear()
        embed = discord.Embed(
            title="✅ Thành Công",
            description="Đã dừng tất cả spam.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_nhay(self, interaction: discord.Interaction, channel_ids: str, delay: str):
        channels = [bot.get_channel(int(channel_id.strip())) for channel_id in channel_ids.split(",")]

        try:
            with open("nhay.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="Không tìm thấy file nhay.txt.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        async def nhay_in_channel(channel):
            while True:
                for line in lines:
                    await channel.send(line.strip())
                    await asyncio.sleep(int(delay))

        nhay_tasks = {}
        for channel in channels:
            if channel and channel.id not in nhay_tasks:
                nhay_task = bot.loop.create_task(nhay_in_channel(channel))
                nhay_tasks[channel.id] = nhay_task
            else:
                embed = discord.Embed(
                    title="⚠️ Lỗi",
                    description=f"Đang có task nhay cho kênh {channel.name}.",
                    color=discord.Color.from_rgb(255, 0, 0)
                )
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title="✅ Thành Công",
            description=f"Đã bắt đầu nhay cho các kênh: {', '.join([channel.name for channel in channels if channel])}.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def execute_stopnhay(self, interaction: discord.Interaction, channel_id: str = None):
        if channel_id:
            channel = bot.get_channel(int(channel_id))
            if channel and channel.id in nhay_tasks:
                nhay_tasks[channel.id].cancel()
                del nhay_tasks[channel.id]
                embed = discord.Embed(
                    title="✅ Thành Công",
                    description=f"Đã dừng nhay cho kênh {channel.name}.",
                    color=discord.Color.from_rgb(0, 102, 204)
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Lỗi",
                    description="Không tìm thấy task nhay cho kênh này.",
                    color=discord.Color.from_rgb(255, 0, 0)
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            for task in nhay_tasks.values():
                task.cancel()
            nhay_tasks.clear()
            embed = discord.Embed(
                title="✅ Thành Công",
                description="Đã dừng tất cả các task nhay.",
                color=discord.Color.from_rgb(0, 102, 204)
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command()
async def menu(ctx):
    view = NgQuangHuyMenu()
    await view.ngquanghuy_dzi_add_buttons()
    msg = await ctx.send(embed=view.pages[0], view=view)
    await asyncio.sleep(300)
    try:
        await msg.delete()
    except discord.NotFound:
        pass

@bot.command()
async def ngquanghuy_dzi_setngonmess(ctx):
    if ctx.author.id not in ng_quang_huy_list and ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng bot này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    if not ctx.message.attachments:
        embed = discord.Embed(
            title="⚠️ Lỗi Đầu Vào",
            description="Vui lòng đính kèm file .txt.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".txt"):
        embed = discord.Embed(
            title="⚠️ Lỗi Định Dạng",
            description="Bot chỉ chấp nhận file .txt.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    path = f"{ctx.author.id}_{attachment.filename}"
    await attachment.save(path)
    embed = discord.Embed(
        title="✅ Thành Công",
        description=f"Đã lưu file thành công dưới tên: `{path}`.",
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_ngonmess(ctx, idbox: str, cookie: str, filename: str, delay: int):
    if ctx.author.id not in ng_quang_huy_list and ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng bot này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    filepath = f"{ctx.author.id}_{filename}"
    if not os.path.exists(filepath):
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Không tìm thấy file đã set.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    with open(filepath, "r", encoding="utf-8") as f:
        message = f.read()
    result = ngquanghuy_dzi_start_spam(ctx.author.id, idbox, cookie, message, delay)
    embed = discord.Embed(
        title="✅ Thành Công",
        description=result,
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_stopngonmess(ctx, idbox: str):
    removed = False
    keys_to_remove = [(uid, ib) for (uid, ib) in treo_threads if uid == ctx.author.id and ib == idbox]
    for key in keys_to_remove:
        treo_threads.pop(key)
        treo_start_times.pop(key)
        messenger_instances.pop(key)
        removed = True
    embed = discord.Embed(
        title="✅ Thành Công" if removed else "⚠️ Lỗi",
        description=f"Đã dừng các tab treo với idbox: `{idbox}`." if removed else "Không có tab treo nào.",
        color=discord.Color.from_rgb(0, 102, 204) if removed else discord.Color.from_rgb(255, 0, 0)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_tabngonmess(ctx):
    msg = "**Danh Sách Tab Treo**\n\n"
    count = 0
    for (uid, ib), start in treo_start_times.items():
        if uid == ctx.author.id:
            uptime = ngquanghuy_dzi_format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "**[NG QUANG HUY BOT]** Bạn không có tab treo nào đang chạy."
    embed = discord.Embed(
        title="📋 Danh Sách Tab Treo",
        description=msg,
        color=discord.Color.from_rgb(106, 13, 173)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_addadmin(ctx, member: discord.Member):
    if ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng lệnh này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    if member.id not in ng_quang_huy_list:
        ng_quang_huy_list.append(member.id)
        embed = discord.Embed(
            title="✅ Thành Công",
            description=f"Đã thêm `{member.name}` vào danh sách ng quang huy.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
    else:
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Người này đã là ng quang huy rồi.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_xoaadmin(ctx, member: discord.Member):
    if ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng lệnh này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    if member.id in ng_quang_huy_list and member.id != IDNG_QUANG_HUY_GOC:
        ng_quang_huy_list.remove(member.id)
        to_remove = [task_id for task_id, info in task_info.items() if info["ng_quang_huy_id"] == member.id]
        for task_id in to_remove:
            if task_id in running_tasks:
                running_tasks[task_id].cancel()
                del running_tasks[task_id]
            del task_info[task_id]
        embed = discord.Embed(
            title="✅ Thành Công",
            description=f"Đã xoá `{member.name}` khỏi danh sách ng quang huy.\nĐã dừng tất cả các task do `{member.name}` tạo.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
    else:
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Không thể xoá ng quang huy gốc hoặc người này không phải ng quang huy.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_listngquanghuy(ctx):
    embed = discord.Embed(
        title="📜 Danh Sách Ng Quang Huy",
        description="Danh sách các ng quang huy hiện tại của bot.",
        color=discord.Color.from_rgb(106, 13, 173)
    )

    for ng_quang_huy_id in ng_quang_huy_list:
        try:
            user = await bot.fetch_user(ng_quang_huy_id)
            if ng_quang_huy_id == IDNG_QUANG_HUY_GOC:
                embed.add_field(name=f"🛡️ {user.name}", value="(Ng Quang Huy Gốc)", inline=False)
            else:
                embed.add_field(name=f"🔹 {user.name}", value="(Ng Quang Huy)", inline=False)
        except Exception:
            embed.add_field(name=f"🔴 {ng_quang_huy_id}", value="(Không tìm được tên)", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_nhaymess(ctx, idbox: str, cookie: str, delay: int):
    if ctx.author.id not in ng_quang_huy_list and ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng bot này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    result = ngquanghuy_dzi_start_nhay(ctx.author.id, idbox, cookie, delay)
    embed = discord.Embed(
        title="✅ Thành Công",
        description=result,
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_stopnhaymess(ctx, idbox: str):
    key = (ctx.author.id, idbox)
    if key in nhay_threads:
        nhay_threads.pop(key)
        nhay_start_times.pop(key)
        embed = discord.Embed(
            title="✅ Thành Công",
            description=f"Đã dừng nhây id box `{idbox}`.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
    else:
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Không có lệnh nhây nào đang chạy.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_tabnhaymess(ctx):
    msg = "**Danh Sách Tab Nhây**\n\n"
    count = 0
    for (uid, ib), start in nhay_start_times.items():
        if uid == ctx.author.id:
            uptime = ngquanghuy_dzi_format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "**[NG QUANG HUY BOT]** Bạn không có tab nhây nào đang chạy."
    embed = discord.Embed(
        title="📋 Danh Sách Tab Nhây",
        description=msg,
        color=discord.Color.from_rgb(106, 13, 173)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_ideamess(ctx, idbox: str, cookie: str, delay: int):
    if ctx.author.id not in ng_quang_huy_list and ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng bot này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    result = ngquanghuy_dzi_start_chui(ctx.author.id, idbox, cookie, delay)
    embed = discord.Embed(
        title="✅ Thành Công",
        description=result,
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_stopideamess(ctx, idbox: str):
    key = (ctx.author.id, idbox)
    if key in chui_threads:
        chui_threads.pop(key)
        chui_start_times.pop(key)
        embed = discord.Embed(
            title="✅ Thành Công",
            description=f"Đã dừng chửi id box `{idbox}`.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
    else:
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Không có lệnh chửi nào đang chạy.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_tabideamess(ctx):
    msg = "**Danh Sách Tab Chửi**\n\n"
    count = 0
    for (uid, ib), start in chui_start_times.items():
        if uid == ctx.author.id:
            uptime = ngquanghuy_dzi_format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "**[NG QUANG HUY BOT]** Bạn không có tab chửi nào đang chạy."
    embed = discord.Embed(
        title="📋 Danh Sách Tab Chửi",
        description=msg,
        color=discord.Color.from_rgb(106, 13, 173)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_codelag(ctx, idbox: str, cookie: str, delay: int):
    if ctx.author.id not in ng_quang_huy_list and ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng bot này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    result = ngquanghuy_dzi_start_codelag(ctx.author.id, idbox, cookie, delay)
    embed = discord.Embed(
        title="✅ Thành Công",
        description=result,
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_stopcodelag(ctx, idbox: str):
    key = (ctx.author.id, idbox)
    if key in codelag_threads:
        codelag_threads.pop(key)
        codelag_start_times.pop(key)
        embed = discord.Embed(
            title="✅ Thành Công",
            description=f"Đã dừng spam code lag vào {idbox}.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
    else:
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Không có tab code lag nào đang chạy.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_tabcodelag(ctx):
    msg = "**Danh Sách Tab Code Lag**\n\n"
    count = 0
    for (uid, ib), start in codelag_start_times.items():
        if uid == ctx.author.id:
            uptime = ngquanghuy_dzi_format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "**[NG QUANG HUY BOT]** Bạn không có tab code lag nào đang chạy."
    embed = discord.Embed(
        title="📋 Danh Sách Tab Code Lag",
        description=msg,
        color=discord.Color.from_rgb(106, 13, 173)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_so(ctx, idbox: str, cookie: str, delay: int):
    if ctx.author.id not in ng_quang_huy_list and ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng bot này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    result = ngquanghuy_dzi_start_so(ctx.author.id, idbox, cookie, delay)
    embed = discord.Embed(
        title="✅ Thành Công",
        description=result,
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_stopso(ctx, idbox: str):
    key = (ctx.author.id, idbox)
    if key in so_threads:
        so_threads.pop(key)
        so_start_times.pop(key)
        embed = discord.Embed(
            title="✅ Thành Công",
            description=f"Đã dừng thả sớ vào {idbox}.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
    else:
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Không có tab sớ nào đang chạy.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_tabso(ctx):
    msg = "**Danh Sách Tab Sớ**\n\n"
    count = 0
    for (uid, ib), start in so_start_times.items():
        if uid == ctx.author.id:
            uptime = ngquanghuy_dzi_format_duration(time.time() - start)
            msg += f"**{ib}:** {uptime}\n"
            count += 1
    if count == 0:
        msg = "**[NG QUANG HUY BOT]** Bạn không có tab sớ nào đang chạy."
    embed = discord.Embed(
        title="📋 Danh Sách Tab Sớ",
        description=msg,
        color=discord.Color.from_rgb(106, 13, 173)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_spam(ctx, ids: str, delay: int, *, content: str):
    if ctx.author.id not in ng_quang_huy_list and ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng bot này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    
    channel_ids = [int(id.strip()) for id in ids.split(",")]

    async def spam_channel(channel_id):
        try:
            channel = bot.get_channel(channel_id)
            if channel:
                while True:
                    await channel.send(content)
                    await asyncio.sleep(delay)
        except Exception as e:
            print(f"Lỗi khi spam kênh {channel_id}: {e}")

    spamming_tasks = []
    for cid in channel_ids:
        task = bot.loop.create_task(spam_channel(cid))
        spamming_tasks.append(task)

    embed = discord.Embed(
        title="✅ Thành Công",
        description="Đã bắt đầu spam.",
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_stopspam(ctx):
    if ctx.author.id not in ng_quang_huy_list and ctx.author.id != IDNG_QUANG_HUY_GOC:
        embed = discord.Embed(
            title="🚫 Lỗi Quyền Hạn",
            description="Bạn không có quyền sử dụng bot này.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)
    
    for task in spamming_tasks:
        task.cancel()
    spamming_tasks.clear()
    embed = discord.Embed(
        title="✅ Thành Công",
        description="Đã dừng tất cả spam.",
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_nhay(ctx, channel_ids: str, delay: int):
    channels = [bot.get_channel(int(channel_id.strip())) for channel_id in channel_ids.split(",")]

    try:
        with open("nhay.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Không tìm thấy file nhay.txt.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        return await ctx.send(embed=embed)

    async def nhay_in_channel(channel):
        while True:
            for line in lines:
                await channel.send(line.strip())
                await asyncio.sleep(delay)

    nhay_tasks = {}
    for channel in channels:
        if channel and channel.id not in nhay_tasks:
            nhay_task = bot.loop.create_task(nhay_in_channel(channel))
            nhay_tasks[channel.id] = nhay_task
        else:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description=f"Đang có task nhay cho kênh {channel.name}.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
            return await ctx.send(embed=embed)

    embed = discord.Embed(
        title="✅ Thành Công",
        description=f"Đã bắt đầu nhay cho các kênh: {', '.join([channel.name for channel in channels if channel])}.",
        color=discord.Color.from_rgb(0, 102, 204)
    )
    await ctx.send(embed=embed)

@bot.command()
async def ngquanghuy_dzi_stopnhay(ctx, channel_id: str = None):
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel and channel.id in nhay_tasks:
            nhay_tasks[channel.id].cancel()
            del nhay_tasks[channel.id]
            embed = discord.Embed(
                title="✅ Thành Công",
                description=f"Đã dừng nhay cho kênh {channel.name}.",
                color=discord.Color.from_rgb(0, 102, 204)
            )
        else:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description="Không tìm thấy task nhay cho kênh này.",
                color=discord.Color.from_rgb(255, 0, 0)
            )
        await ctx.send(embed=embed)
    else:
        for task in nhay_tasks.values():
            task.cancel()
        nhay_tasks.clear()
        embed = discord.Embed(
            title="✅ Thành Công",
            description="Đã dừng tất cả các task nhay.",
            color=discord.Color.from_rgb(0, 102, 204)
        )
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Lệnh không tồn tại. Vui lòng sử dụng `.menu` để xem danh sách lệnh.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description="Thiếu tham số cần thiết. Vui lòng kiểm tra lại cú pháp lệnh.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    else:
        embed = discord.Embed(
            title="⚠️ Lỗi",
            description=f"Đã xảy ra lỗi: {str(error)}",
            color=discord.Color.from_rgb(255, 0, 0)
        )
    await ctx.send(embed=embed)

bot.run(TOKEN)