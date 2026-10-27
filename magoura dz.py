"""
╔══════════════════════════════════════════════════════════════════╗
║ OOREDOO BUNDLE & GIFT MANAGEMENT BOT - ULTRA FAST & SECURED      ║
║ NEXION Bot2 - VERSION 1.5.17 FULLY STABLE & SAFE (FIXED)         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from requests.adapters import HTTPAdapter
import json, os, threading, re, sys, uuid, base64, time, urllib.parse
from datetime import datetime, timezone
import urllib3
from concurrent.futures import ThreadPoolExecutor
from telebot.apihelper import ApiTelegramException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOT_TOKEN = "8768046493:AAHP71F3VXHGRexAnbc3CdkRMG_l0HdmFQE"
ADMIN_IDS = [7757737178]
NOTIFY_CHANNEL_ID = "@salahdz112"  # القيمة الافتراضية، تُعدَّل من /admin

# قائمة قنوات الاشتراك الإجباري
FORCE_SUB_CHANNELS = [
    {"channel": "@salah_dz_13", "link": "https://t.me/salah_dz_13"},
]
DEFAULT_MAX_ACTIVATIONS = 2  # الحد الأقصى للتفعيل خلال 24 ساعة (يُعدَّل من /admin)

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
executor = ThreadPoolExecutor(max_workers=128)

OOREDOO_BFF = "https://apis.ooredoo.dz/api/ooredoo-bff"
OOREDOO_AUTH = "https://apis.ooredoo.dz/api/auth/realms/myooredoo/protocol/openid-connect/token"
OOREDOO_CLIENT_ID = "myooredoo-app"
OOREDOO_X_VERSION = "1.5.17"
OOREDOO_X_SIG = "5c7641dbb82cf11066df68afc91541c967640106a95192740b43d51a5ce6777a"
OOREDOO_PLATFORM = "android"
OOREDOO_PLATFORM_ORIGIN = "mobile-android"

OOREDOO_INTEGRITY_1 = "JWBTpxXcH7KY9EXYeIRp8NjQMx2dt3vF8ejjoARazyoFzOw6Cu8+wkeV+zSVHSTeI6a12SG/FU+Q/9uBrcN71RlYO4CulD2x375NKwJRAInar8DVUilHBKUfjEsoHd6EwfLCfdYzLNXJu9POfEf6tqKn3PUe0pY6qZxWLhyVAFHw8Qwb52ZqdI2soCH4S3mrz+OZL+YovdGSUKlXKIkxVroAMTAg3jljLF7gvXaEsB/O3uW+tbkBMwSX2uTOwf+rh3sgOF/zPhKCFgRvZmU1o87Fa96Y/+wOcK+UpfXTCBYVrvQ1wG6ryC7vHMSqgUhYJK4tbSoti0zv4av9pwxh9Iv2MgsMENjyKBK/TuFZxEG3xQCKj1LTMgn2xBEeKcbsKrEW3xDRwsccGI3D7GHnbUlhdI4ujDIRQVKHaZSwhTp+32Cr4EB/Qt8p/xRbdgCde9MUlM4AYIGlfyVoHSkOvTu5c0DIIy1EhowtAkbKIJl49wsYKWvpT/nXFWzeXP3R2qzaclCnIb9qihhrarmwz8l8XH2T+f7AK2uSNiuWLG5Fy2mM/YLmuJPZT9Ciag/mpy7JGImKNQAcFbSAInBdKQjUKT+COzZfrXj5rwil9/HDMtuzIovq8hrQGY+roTfVPheTLWmcjkVCOL8VXAHjPb22vOuqrkMioWT9CQ5O8RgW7RKHrObeKQMp8F7tSjOqkxYDFkPVN1G4nkEBrTlPKK9YtPl+j7IuH9fGcDTwhCTTqP8peuBryW0L11tApvAEi7VkJyBxpVxW"
OOREDOO_INTEGRITY_2 = "JWBTpxXcH7KR/kzaHeUUydDWODuU4i3H4fL9gCgKzyYfyN4qLJJE8keV+zSVHSTeI6aEyC2tbSza/NGmkflQ/UgaNZSN9SKxz7tcdQckHY25n6mOaDZ9PPMQmF4sKZqDwebce/c1SNGNn6qvTULW/L348aJvy7Vii6dyPTu3OSPV9AwKwGwQKNHN61HyK3jx/fa8Os5ux9u3Q654YLZrAJ99QGEm/C9nEBPmlHC98RjovLGBnuJOGx6k7fnyrt/Ogy5fNg+tBgi5HEsoXDAwutX7TOWfx4YKHpKW//TvPRQgp69e2Xqa+CvGJJ+a/WlPMPhRCSsfo0OG04mVvlkc8eXiLzV/GPuJCEmcRf9Z6V+xoDyMtU7OZ3XT5BMhI/D/N68LsRn/9dIBH6X7n0WAW3tzeKZK1zENWFKrd7aLlzEdwFzO/1JTQsEDom5TRie0Kd5yic4BGvS1C1BsA2wJhzyiZ2j7RUE9m8tOAkPEIs929FYIfmH8XcCQKHT0TqT0+N+wCiyfNawPlDhZWcObscFZeEmKgvqiUFCoCj6xI1hvyHK0nu7fnZ/sGc6oNT/SrFjubYWjOyoYFL7gMnlYAhyjZhjuAwN1m1/wjwrOx8DbFr2NW8qb3hv+CIzK1zL3LDryKjqNkTxcOp4aJnmSTa73guCEmWc7pnLkLw5O8RgW7RKHrObeeQ0l9lu4HWXwlhdWRxvVMQDimhtTrGASL6sIuaxyhOkrH4HFImP70SaCoK9+euMxnzkPjg9HqPIFj+I0KSMloVxW"

OOREDOO_PROXIES = [
    "gate.busyip.com:18080:bi_23ee2cd9-session-s1-type-residential-mode-sticky:9C0h1L16DX5gwKbv",
]

OOREDOO_USERS_FILE = "ooredoo_users.json"
ACTIVATIONS_FILE = "ooredoo_activations.json"

ooredoo_data = {}
activations_data = {}

http_session = requests.Session()
adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200, max_retries=1)
http_session.mount("https://", adapter)
http_session.mount("http://", adapter)

file_lock = threading.Lock()
activations_lock = threading.Lock()

# ══════════════════════════════════════════════════════════════════
#  الإعدادات القابلة للتعديل من لوحة الأدمن (تُحفظ في bot_settings.json)
# ══════════════════════════════════════════════════════════════════
SETTINGS_FILE = "bot_settings.json"
KNOWN_USERS_FILE = "bot_known_users.json"
settings_lock = threading.RLock()

bot_settings = {
    "notify_channel": NOTIFY_CHANNEL_ID,
    "force_sub_channels": [dict(c) for c in FORCE_SUB_CHANNELS],
    "max_activations": DEFAULT_MAX_ACTIVATIONS,
    "activation_cooldown": 0,  # الفاصل الزمني بين كل تفعيل (بالثواني) - 0 = معطّل
    "bot_enabled": True,  # تشغيل/إيقاف البوت للمستخدمين (الأدمن يبقى يعمل دائماً)
    "banned_users": [],  # المستخدمون المحظورون من البوت
    "success_image": None,  # file_id للصورة المرسلة بعد التفعيل الناجح
    "referral_enabled": True,  # تشغيل/إيقاف نظام الإحالة (من لوحة الأدمن)
}
known_users = set()

def parse_channel_input(raw):
    """يقبل @username أو رابط t.me/username أو معرف رقمي -100...
    يرجع (channel_ref, link) أو None. link يكون None للمعرف الرقمي."""
    t = (raw or "").strip()
    if re.fullmatch(r'-100\d{5,}', t):
        return t, None
    m = re.fullmatch(r'(?:https?://)?(?:www\.)?(?:t|telegram)\.me/([A-Za-z][A-Za-z0-9_]{3,})/?', t, re.I)
    if m:
        u = m.group(1)
    elif re.fullmatch(r'@?[A-Za-z][A-Za-z0-9_]{3,}', t):
        u = t.lstrip('@')
    else:
        return None
    return f"@{u}", f"https://t.me/{u}"

def save_settings():
    with settings_lock:
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(bot_settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Settings save error: {e}")

def save_known_users():
    with settings_lock:
        try:
            with open(KNOWN_USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(sorted(known_users), f)
        except Exception as e:
            print(f"Known users save error: {e}")

def load_settings():
    global known_users
    with settings_lock:
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                if d.get("notify_channel"):
                    bot_settings["notify_channel"] = d["notify_channel"]
                if isinstance(d.get("force_sub_channels"), list):
                    bot_settings["force_sub_channels"] = d["force_sub_channels"]
                if isinstance(d.get("max_activations"), int) and d["max_activations"] >= 1:
                    bot_settings["max_activations"] = d["max_activations"]
                if isinstance(d.get("activation_cooldown"), int) and d["activation_cooldown"] >= 0:
                    bot_settings["activation_cooldown"] = d["activation_cooldown"]
                if isinstance(d.get("bot_enabled"), bool):
                    bot_settings["bot_enabled"] = d["bot_enabled"]
                if isinstance(d.get("referral_enabled"), bool):
                    bot_settings["referral_enabled"] = d["referral_enabled"]
                if isinstance(d.get("banned_users"), list):
                    bot_settings["banned_users"] = [int(x) for x in d["banned_users"] if str(x).lstrip("-").isdigit()]
                if isinstance(d.get("success_image"), str) and d["success_image"]:
                    bot_settings["success_image"] = d["success_image"]
            except Exception as e:
                print(f"Settings load error: {e}")

        # تحويل رابط قناة النشر إلى @username (الإرسال لا يعمل بالرابط)
        parsed = parse_channel_input(str(bot_settings["notify_channel"]))
        if parsed:
            bot_settings["notify_channel"] = parsed[0]

        # إزالة القنوات المكررة
        seen, uniq = set(), []
        for c in bot_settings["force_sub_channels"]:
            k = str(c.get("channel", "")).strip()
            if k and k not in seen:
                seen.add(k)
                uniq.append(c)
        bot_settings["force_sub_channels"] = uniq
        save_settings()

        if os.path.exists(KNOWN_USERS_FILE):
            try:
                with open(KNOWN_USERS_FILE, 'r', encoding='utf-8') as f:
                    known_users = {int(x) for x in json.load(f)}
            except Exception:
                known_users = set()

def get_notify_channel():
    with settings_lock:
        return bot_settings["notify_channel"]

def get_force_channels():
    with settings_lock:
        return [dict(c) for c in bot_settings["force_sub_channels"]]

def get_max_activations():
    with settings_lock:
        return int(bot_settings["max_activations"])

def get_activation_cooldown():
    with settings_lock:
        return int(bot_settings.get("activation_cooldown", 0))

def set_activation_cooldown(sec):
    with settings_lock:
        bot_settings["activation_cooldown"] = max(0, int(sec))
        save_settings()

def format_duration(sec):
    """يحوّل الثواني إلى نص عربي مقروء."""
    sec = int(sec)
    if sec <= 0:
        return "معطّل"
    h, rem = divmod(sec, 3600)
    m, s_ = divmod(rem, 60)
    parts = []
    if h: parts.append(f"{h} ساعة")
    if m: parts.append(f"{m} دقيقة")
    if s_: parts.append(f"{s_} ثانية")
    return " و ".join(parts)

def parse_duration(text):
    """يقبل: 30 (دقائق) / 45s / 10m / 2h  -> يرجع عدد الثواني أو None."""
    t = (text or "").strip().lower().replace(" ", "")
    mt = re.fullmatch(r'(\d{1,6})(s|m|h)?', t)
    if not mt:
        return None
    n = int(mt.group(1))
    unit = mt.group(2) or "m"
    return n * {"s": 1, "m": 60, "h": 3600}[unit]

def set_notify_channel(ch):
    with settings_lock:
        bot_settings["notify_channel"] = ch
        save_settings()

def set_max_activations(n):
    with settings_lock:
        bot_settings["max_activations"] = int(n)
        save_settings()

def is_bot_enabled():
    with settings_lock:
        return bool(bot_settings.get("bot_enabled", True))

def set_bot_enabled(enabled):
    with settings_lock:
        bot_settings["bot_enabled"] = bool(enabled)
        save_settings()

BOT_STOPPED_MSG = "🛠 البوت متوقف مؤقتاً، يرجى المحاولة لاحقاً."

BANNED_MSG = "🚫 تم حظرك من استخدام هذا البوت."

def is_blocked(uid):
    if uid in ADMIN_IDS:
        return False
    with settings_lock:
        return uid in bot_settings.get("banned_users", [])

def ban_user(uid):
    with settings_lock:
        if uid not in bot_settings["banned_users"]:
            bot_settings["banned_users"].append(uid)
            save_settings()

def unban_user(uid):
    with settings_lock:
        if uid in bot_settings["banned_users"]:
            bot_settings["banned_users"].remove(uid)
            save_settings()

def get_banned_users():
    with settings_lock:
        return list(bot_settings.get("banned_users", []))

def get_success_image():
    with settings_lock:
        return bot_settings.get("success_image")

def set_success_image(file_id):
    with settings_lock:
        bot_settings["success_image"] = file_id
        save_settings()

def add_force_channel(ch, link):
    with settings_lock:
        if any(str(c["channel"]) == str(ch) for c in bot_settings["force_sub_channels"]):
            return False
        bot_settings["force_sub_channels"].append({"channel": ch, "link": link})
        save_settings()
        return True

def remove_force_channel(index):
    with settings_lock:
        chans = bot_settings["force_sub_channels"]
        if 0 <= index < len(chans):
            removed = chans.pop(index)
            save_settings()
            return removed
        return None

def register_user(uid):
    with settings_lock:
        if uid in known_users:
            return
        known_users.add(uid)
        save_known_users()

def get_all_user_ids():
    with settings_lock:
        return set(known_users) | set(ooredoo_data.keys())

def load_ooredoo_data():
    global ooredoo_data, activations_data
    with file_lock:
        if os.path.exists(OOREDOO_USERS_FILE):
            try:
                with open(OOREDOO_USERS_FILE, 'r', encoding='utf-8') as f:
                    d = json.load(f); ooredoo_data = {int(k): v for k, v in d.items()}
            except: ooredoo_data = {}
        
        if os.path.exists(ACTIVATIONS_FILE):
            try:
                with open(ACTIVATIONS_FILE, 'r', encoding='utf-8') as f:
                    activations_data = json.load(f)
            except: activations_data = {}

def save_ooredoo_data():
    with file_lock:
        with open(OOREDOO_USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({str(k): v for k, v in ooredoo_data.items()}, f, ensure_ascii=False, indent=2)

def save_activations():
    with file_lock:
        with open(ACTIVATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(activations_data, f, ensure_ascii=False, indent=2)

def check_and_record_activation(msisdn):
    """يرجع (allowed, info). info = {"reason": "limit"|"cooldown", "remaining": ثواني}"""
    current_time = time.time()
    with activations_lock:
        acts = [t for t in activations_data.get(msisdn, []) if current_time - t < 86400]
        activations_data[msisdn] = acts

        if len(acts) >= get_max_activations():
            return False, {"reason": "limit", "remaining": 0}

        cd = get_activation_cooldown()
        if cd > 0 and acts:
            elapsed = current_time - max(acts)
            if elapsed < cd:
                return False, {"reason": "cooldown", "remaining": int(cd - elapsed) + 1}

        acts.append(current_time)
        save_activations()
        return True, {"reason": "ok", "remaining": 0}

def refund_activation(msisdn):
    """يلغي آخر تفعيل مسجَّل لأن العملية لم تنجح."""
    with activations_lock:
        acts = activations_data.get(msisdn, [])
        if acts:
            acts.pop()
            save_activations()

def ooredoo_get_user(chat_id): return ooredoo_data.get(chat_id)
def ooredoo_save_user(chat_id, data): ooredoo_data[chat_id] = data; save_ooredoo_data()
def ooredoo_delete_user(chat_id):
    if chat_id in ooredoo_data: del ooredoo_data[chat_id]; save_ooredoo_data()

class OoredooStore:
    def __init__(self):
        self._data = {}; self._expiry = {}; self._lock = threading.Lock()
    def hset(self, key, mapping=None, **kwargs):
        with self._lock:
            if key not in self._data: self._data[key] = {}
            if mapping: self._data[key].update({str(k): str(v) for k, v in mapping.items()})
            if kwargs: self._data[key].update({str(k): str(v) for k, v in kwargs.items()})
    def hgetall(self, key):
        with self._lock: return dict(self._data.get(key, {}))
    def expire(self, key, ttl):
        with self._lock: self._expiry[key] = time.time() + ttl
    def delete(self, key):
        with self._lock: self._data.pop(key, None); self._expiry.pop(key, None)
    def get(self, key):
        with self._lock: 
            if key in self._expiry and time.time() > self._expiry[key]:
                self._data.pop(key, None)
                self._expiry.pop(key, None)
            return self._data.get(key)
    def set(self, key, value, ex=None):
        with self._lock: 
            self._data[key] = value
            if ex: self._expiry[key] = time.time() + ex

ooredoo_store = OoredooStore()

def ooredoo_now_ms(): return str(int(time.time() * 1000))

def ooredoo_new_instance_id():
    u = uuid.uuid4().hex
    return f"{u[:8]}-{u[8:12]}-11{u[12:16]}-{u[16:20]}-{u[20:32]}{ooredoo_now_ms()}"

def ooredoo_new_plat_sig(iid):
    p = json.dumps({"platform": "android", "is-physical-device": True, "device-id": iid}, separators=(',', ':'))
    return base64.b64encode(p.encode()).decode()

def ooredoo_new_corr_id(): return uuid.uuid4().hex + ooredoo_now_ms()
def ooredoo_new_fingerprint(): return uuid.uuid4().hex + uuid.uuid4().hex[:32]

# تم تصحيح الخطأ هنا (msisdn بدلاً من msidsn)
def mask_msisdn(msisdn):
    if not msisdn or len(msisdn) < 4:
        return "********"
    return msisdn[:2] + "*" * (len(msisdn) - 4) + msisdn[-2:]

def ooredoo_parse_proxy(raw):
    try:
        if not raw or not isinstance(raw, str):
            return None
        p = raw.strip().split(":", 3)
        if len(p) >= 4:
            return {"host": f"{p[0]}:{p[1]}", "userpass": f"{p[2]}:{p[3]}"}
        elif len(p) == 2:
            return {"host": f"{p[0]}:{p[1]}", "userpass": ""}
    except Exception as e:
        print(f"Proxy parse error: {e}")
    return None

def get_valid_proxies():
    valid = []
    for p in OOREDOO_PROXIES:
        parsed = ooredoo_parse_proxy(p)
        if parsed:
            valid.append(parsed)
    return valid

def _ooredoo_do_request(method, url, headers, body="", proxy=None, timeout=5):
    proxies = None
    if proxy and proxy.get("host"):
        if proxy.get("userpass"):
            proxies = {"http": f"http://{proxy['userpass']}@{proxy['host']}", "https": f"http://{proxy['userpass']}@{proxy['host']}"}
        else:
            proxies = {"http": f"http://{proxy['host']}", "https": f"http://{proxy['host']}"}
    try:
        if method == "GET": r = http_session.get(url, headers=headers, proxies=proxies, timeout=timeout, verify=False)
        elif method == "HEAD": r = http_session.head(url, headers=headers, proxies=proxies, timeout=timeout, verify=False)
        else: r = http_session.post(url, headers=headers, data=body, proxies=proxies, timeout=timeout, verify=False)
        txt = r.text
        if "<!DOCTYPE" in txt or "<html" in txt: return {"ip_blocked": True, "code": r.status_code}
        try: j = r.json()
        except: j = None
        return {"code": r.status_code, "body": txt, "headers": {k.lower(): v for k, v in r.headers.items()}, "json": j}
    except: return None

def ooredoo_http_request(method, url, headers, body="", proxy=None, timeout=5):
    result = _ooredoo_do_request(method, url, headers, body, proxy, timeout)
    if result is None and proxy is not None:
        result = _ooredoo_do_request(method, url, headers, body, None, timeout)
    return result

def ooredoo_get_session(chat_id):
    data = ooredoo_store.hgetall(f"ooredoo:session:{chat_id}")
    return data if data else {}

def ooredoo_set_session(chat_id, data, ttl=3600):
    cleaned = {k: str(v) for k, v in data.items() if v is not None}
    if cleaned:
        ooredoo_store.hset(f"ooredoo:session:{chat_id}", mapping=cleaned)
        ooredoo_store.expire(f"ooredoo:session:{chat_id}", ttl)

def ooredoo_clear_session(chat_id): ooredoo_store.delete(f"ooredoo:session:{chat_id}")

def ooredoo_get_or_create_device(chat_id):
    raw = ooredoo_store.get(f"ooredoo:device:{chat_id}")
    if raw:
        try:
            d = json.loads(raw)
            if d.get("instance_id") and d.get("plat_sig"): return d
        except: pass
    iid = ooredoo_new_instance_id(); psig = ooredoo_new_plat_sig(iid)
    d = {"instance_id": iid, "plat_sig": psig, "created_at": int(time.time())}
    ooredoo_store.set(f"ooredoo:device:{chat_id}", json.dumps(d))
    return d

def ooredoo_base_headers(msisdn, fp, corr, ts, iid, psig):
    return {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
            "x-device-fingerprint": fp, "x-platform-origin": OOREDOO_PLATFORM_ORIGIN,
            "x-correlation-id": corr, "platform": OOREDOO_PLATFORM, "x-version": OOREDOO_X_VERSION,
            "x-signature": OOREDOO_X_SIG, "x-platform-data-signature": psig,
            "x-timestamp": ts, "x-instance-id": iid}

def ooredoo_authed_headers_web(msisdn, token, tok_hdrs):
    ts = tok_hdrs.get("tok_timestamp") or ooredoo_now_ms()
    iid = tok_hdrs.get("tok_instance_id") or ooredoo_new_instance_id()
    psig = tok_hdrs.get("tok_plat_sig") or ooredoo_new_plat_sig(iid)
    return {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
            "x-device-fingerprint": ooredoo_new_fingerprint(), "x-platform-origin": "web",
            "authorization": f"Bearer {token}", "x-correlation-id": ooredoo_new_corr_id(),
            "platform": "web", "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
            "x-platform-data-signature": psig, "x-timestamp": ts, "x-instance-id": iid,
            "origin": "https://my.ooredoo.dz", "referer": "https://my.ooredoo.dz/"}

def ooredoo_token_proxy(user):
    host = user.get("token_proxy_host", "direct"); up = user.get("token_proxy_user", "")
    if host == "direct" or not host: return None
    return {"host": host, "userpass": up}

def ooredoo_tok_hdrs(user):
    return {"tok_timestamp": user.get("tok_timestamp"), "tok_instance_id": user.get("tok_instance_id"), "tok_plat_sig": user.get("tok_plat_sig")}

def check_user_subscription(user_id):
    for item in get_force_channels():
        ch = item["channel"]
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            continue
    return True

def get_subscription_markup():
    markup = InlineKeyboardMarkup()
    for item in get_force_channels():
        markup.add(InlineKeyboardButton(f"📢 اشترك في القناة", url=item['link']))
    markup.add(InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub"))
    return markup

def _otp_dbg(step, proxy, r):
    host = proxy["host"] if proxy else "direct"
    if r is None:
        print(f"[OTP] {step} via {host}: no response (timeout/connection error)")
    else:
        print(f"[OTP] {step} via {host}: code={r.get('code')} ip_blocked={bool(r.get('ip_blocked'))}")

def ooredoo_send_otp(msisdn, device):
    try:
        iid = device["instance_id"]; psig = device["plat_sig"]
        all_proxies = get_valid_proxies() + [None]
        for proxy in all_proxies:
            ts, corr = ooredoo_now_ms(), ooredoo_new_corr_id()
            h1 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
            r1 = ooredoo_http_request("GET", f"{OOREDOO_BFF}/users/status?msisdn={msisdn}", h1, proxy=proxy, timeout=8)
            _otp_dbg("status", proxy, r1)
            if not r1 or r1.get("ip_blocked") or r1.get("code") != 200: continue

            h2 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), ooredoo_new_corr_id(), ooredoo_now_ms(), iid, psig)
            r2 = ooredoo_http_request("HEAD", f"{OOREDOO_BFF}/userInfo?msisdn={msisdn}", h2, proxy=proxy, timeout=8)
            _otp_dbg("userInfo", proxy, r2)
            if not r2 or r2.get("ip_blocked") or r2.get("code") not in (200, 204): continue

            for p34 in all_proxies:
                ts = ooredoo_now_ms(); corr = ooredoo_new_corr_id()
                h3 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
                h3["content-type"] = "application/json; charset=utf-8"
                h3["x-native-integrity-token"] = OOREDOO_INTEGRITY_1
                h3["x-path"] = "/api/auth/realms/myooredoo/protocol/openid-connect/token"
                h3["x-method"] = "POST"
                r3 = ooredoo_http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, body="{}", proxy=p34, timeout=8)
                _otp_dbg("checkpoint", p34, r3)
                if not r3 or r3.get("ip_blocked"): continue
                nonce = r3.get("headers", {}).get("x-nonce-id")
                chronos = r3.get("headers", {}).get("x-chronos-id")
                if not nonce or not chronos:
                    print("[OTP] checkpoint: missing x-nonce-id / x-chronos-id headers")
                    continue
                h4 = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
                      "x-device-fingerprint": ooredoo_new_fingerprint(), "x-nonce-id": nonce,
                      "x-platform-origin": OOREDOO_PLATFORM_ORIGIN, "platform": OOREDOO_PLATFORM,
                      "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
                      "x-chronos-id": chronos, "x-timestamp": ts, "x-platform-info": psig,
                      "x-force-update": "true", "x-instance-id": iid,
                      "Content-Type": "application/x-www-form-urlencoded"}
                body4 = urllib.parse.urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "password", "username": msisdn})
                r4 = ooredoo_http_request("POST", OOREDOO_AUTH, h4, body=body4, proxy=p34, timeout=8)
                _otp_dbg("token(send-otp)", p34, r4)
                if r4 and r4.get("code") in (401, 403):
                    return {"proxy": p34}
        print("[OTP] all attempts failed")
    except Exception as e:
        print(f"[OTP] exception while sending: {e!r}")
    return None

def _verify_otp_once(msisdn, otp, proxy, device):
    """محاولة واحدة للتحقق عبر بروكسي محدد. ترجع dict عند النجاح، أو "wrong_otp"، أو None."""
    iid = device["instance_id"]; psig = device["plat_sig"]
    ts = ooredoo_now_ms(); corr = ooredoo_new_corr_id()
    h6 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
    h6["content-type"] = "application/json; charset=utf-8"
    h6["x-native-integrity-token"] = OOREDOO_INTEGRITY_2
    h6["x-path"] = "/api/auth/realms/myooredoo/protocol/openid-connect/token"
    h6["x-method"] = "POST"
    r6 = ooredoo_http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h6, body="{}", proxy=proxy, timeout=8)
    _otp_dbg("verify-checkpoint", proxy, r6)
    if not r6 or r6.get("ip_blocked"):
        return None
    nonce2 = r6.get("headers", {}).get("x-nonce-id")
    chronos2 = r6.get("headers", {}).get("x-chronos-id")
    if not nonce2 or not chronos2:
        print("[OTP] verify checkpoint: missing x-nonce-id / x-chronos-id headers")
        return None
    fp7 = ooredoo_new_fingerprint()
    h7 = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
          "x-device-fingerprint": fp7, "x-nonce-id": nonce2, "x-platform-origin": OOREDOO_PLATFORM_ORIGIN,
          "platform": OOREDOO_PLATFORM, "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
          "x-chronos-id": chronos2, "x-timestamp": ts, "x-platform-info": psig,
          "x-force-update": "true", "x-instance-id": iid, "Content-Type": "application/x-www-form-urlencoded"}
    body7 = urllib.parse.urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "password", "username": msisdn, "otp": otp})
    r7 = ooredoo_http_request("POST", OOREDOO_AUTH, h7, body=body7, proxy=proxy, timeout=8)
    _otp_dbg("verify-token", proxy, r7)
    if not r7 or r7.get("ip_blocked"):
        return None
    if r7.get("code") in (401, 403):
        return "wrong_otp"
    if r7.get("code") == 200 and r7.get("json") and "access_token" in r7["json"]:
        j = r7["json"]
        return {"access_token": j["access_token"], "refresh_token": j.get("refresh_token", ""),
                "token_proxy_host": proxy["host"] if proxy else "direct",
                "token_proxy_user": proxy["userpass"] if proxy else "",
                "tok_fingerprint": fp7, "tok_timestamp": ts, "tok_instance_id": iid,
                "tok_plat_sig": psig, "tok_correlation": corr}
    print(f"[OTP] verify token: unexpected code={r7.get('code')}")
    return None

def ooredoo_verify_otp(msisdn, otp, proxy, device):
    """يجرب البروكسي الذي أُرسل عبره الرمز أولاً، ثم بقية البروكسيات والاتصال المباشر."""
    try:
        cands = []
        if proxy and proxy.get("host"):
            cands.append(proxy)
        for p in get_valid_proxies() + [None]:
            if p is None or not any(c["host"] == p["host"] for c in cands):
                cands.append(p)
        for p in cands:
            res = _verify_otp_once(msisdn, otp, p, device)
            if res == "wrong_otp" or isinstance(res, dict):
                return res
        print("[OTP] verify: all attempts failed")
    except Exception as e:
        print(f"[OTP] exception while verifying: {e!r}")
    return None

def ooredoo_refresh_token(chat_id, user, device):
    try:
        rt = user.get("refresh_token", ""); msisdn = user.get("msisdn", "")
        if not rt: return "expired"
        iid = device["instance_id"]; psig = device["plat_sig"]; ts = ooredoo_now_ms()
        h = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip",
             "Content-Type": "application/x-www-form-urlencoded", "x-msisdn": msisdn,
             "x-platform-origin": OOREDOO_PLATFORM_ORIGIN, "platform": OOREDOO_PLATFORM,
             "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
             "x-platform-data-signature": psig, "x-timestamp": ts, "x-instance-id": iid}
        body = urllib.parse.urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "refresh_token", "refresh_token": rt})
        r = ooredoo_http_request("POST", OOREDOO_AUTH, h, body=body, proxy=ooredoo_token_proxy(user), timeout=5)
        if not r: return False
        if r.get("code") == 400 and (r.get("json") or {}).get("error") == "invalid_grant": return "expired"
        if r.get("code") == 200 and r.get("json") and "access_token" in r["json"]:
            j = r["json"]
            return {"access_token": j["access_token"], "refresh_token": j.get("refresh_token", rt),
                    "token_proxy_host": user.get("token_proxy_host", "direct"),
                    "token_proxy_user": user.get("token_proxy_user", ""),
                    "tok_fingerprint": ooredoo_new_fingerprint(), "tok_timestamp": ts,
                    "tok_instance_id": iid, "tok_plat_sig": psig, "tok_correlation": ooredoo_new_corr_id()}
    except Exception:
        pass
    return False

def ooredoo_check_power_snake(msisdn, user):
    try:
        token = user.get("access_token")
        proxy = ooredoo_token_proxy(user)
        hp = ooredoo_authed_headers_web(msisdn, token, ooredoo_tok_hdrs(user))
        hp["accept"] = "application/json"
        r = ooredoo_http_request("GET", f"{OOREDOO_BFF}/gamification/power-snake?status=AVAILABLE", hp, proxy=proxy, timeout=5)
        if r and r.get("code") == 200 and r.get("json"): return r.get("json")
    except Exception:
        pass
    return None

def ooredoo_redeem_power_snake(msisdn, user, uuid_str):
    try:
        token = user.get("access_token")
        proxy = ooredoo_token_proxy(user)
        tok_hdrs = ooredoo_tok_hdrs(user)
        ts = ooredoo_now_ms()
        corr = ooredoo_new_corr_id()
        iid = tok_hdrs.get("tok_instance_id") or ooredoo_new_instance_id()
        psig = tok_hdrs.get("tok_plat_sig") or ooredoo_new_plat_sig(iid)

        h3 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
        h3["content-type"] = "application/json; charset=utf-8"
        h3["x-native-integrity-token"] = OOREDOO_INTEGRITY_1
        h3["x-path"] = f"/api/ooredoo-bff/gamification/power-snake/{uuid_str}/redeem"
        h3["x-method"] = "POST"
        r3 = ooredoo_http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, body="{}", proxy=proxy, timeout=5)
        nonce = (r3.get("headers") or {}).get("x-nonce-id") if r3 else None
        chronos = (r3.get("headers") or {}).get("x-chronos-id") if r3 else None
        
        hp = ooredoo_authed_headers_web(msisdn, token, tok_hdrs)
        if nonce: hp["x-nonce-id"] = nonce
        if chronos: hp["x-chronos-id"] = chronos
        hp["content-type"] = "application/json"
        hp["accept"] = "application/json"
        
        rp = ooredoo_http_request("POST", f"{OOREDOO_BFF}/gamification/power-snake/{uuid_str}/redeem", hp, body="", proxy=proxy, timeout=10)
        if not rp: return {"success": False}
        code = rp.get("code")
        if code in (200, 201):
            j = rp.get("json") or {}
            reward_info = j.get("assignedReward", {})
            reward_detail = reward_info.get("reward", {})
            val = reward_detail.get("usage-value", "")
            unit = reward_detail.get("usage-unit", "")
            validity = reward_detail.get("validity", "3")
            return {"success": True, "reward": f"{val} {unit}", "validity": validity}
    except Exception:
        pass
    return {"success": False}

def _bundle_log(step, r):
    if r is None:
        print(f"[BUNDLE] {step}: no response (timeout/connection error)")
    else:
        print(f"[BUNDLE] {step}: code={r.get('code')} body={str(r.get('body', ''))[:300]}")

def _bundle_purchase_ok(r):
    """يعتبر الشراء ناجحاً فقط عند رد 200/201 بدون حقل خطأ في الـ JSON."""
    if not r or r.get("code") not in (200, 201):
        return False
    j = r.get("json")
    if isinstance(j, dict) and ("error" in j or "errorCode" in j):
        return False
    return True

def ooredoo_activate_target_bundle(msisdn, user, _retry=False):
    try:
        token = user.get("access_token")
        proxy = ooredoo_token_proxy(user)
        tok_hdrs = ooredoo_tok_hdrs(user)
        ts = ooredoo_now_ms()
        corr = ooredoo_new_corr_id()
        iid = tok_hdrs.get("tok_instance_id") or ooredoo_new_instance_id()
        psig = tok_hdrs.get("tok_plat_sig") or ooredoo_new_plat_sig(iid)

        h3 = ooredoo_base_headers(msisdn, ooredoo_new_fingerprint(), corr, ts, iid, psig)
        h3["content-type"] = "application/json; charset=utf-8"
        h3["x-native-integrity-token"] = OOREDOO_INTEGRITY_1
        h3["x-path"] = "/api/ooredoo-bff/bundle/bundlePurchase/v2"
        h3["x-method"] = "POST"

        r3 = ooredoo_http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, body="{}", proxy=proxy, timeout=10)
        nonce = (r3.get("headers") or {}).get("x-nonce-id") if r3 else None
        chronos = (r3.get("headers") or {}).get("x-chronos-id") if r3 else None

        hp = ooredoo_authed_headers_web(msisdn, token, tok_hdrs)
        if nonce: hp["x-nonce-id"] = nonce
        if chronos: hp["x-chronos-id"] = chronos
        hp["content-type"] = "application/json; charset=utf-8"
        hp["x-version"] = OOREDOO_X_VERSION

        payload = {
            "msisdn": msisdn,
            "bundleCode": "DATA_1000_KTM"
        }

        rp = ooredoo_http_request("POST", f"{OOREDOO_BFF}/bundle/bundlePurchase/v2", hp, body=json.dumps(payload), proxy=proxy, timeout=10)
        _bundle_log("bundlePurchase", rp)

        # انتهت صلاحية التوكن: نجدده مرة واحدة فقط لتفادي التكرار اللانهائي
        if rp and rp.get("code") == 401 and not _retry:
            device = ooredoo_get_or_create_device(msisdn)
            new_tok = ooredoo_refresh_token(msisdn, user, device)
            if isinstance(new_tok, dict):
                user.update(new_tok)
                return ooredoo_activate_target_bundle(msisdn, user, _retry=True)

        purchase_ok = _bundle_purchase_ok(rp)

        # محاولة استلام المكافأة الفعلية (power snake)
        snake_data = ooredoo_check_power_snake(msisdn, user)
        _bundle_log("power-snake-check", {"code": 200 if snake_data else None, "body": json.dumps(snake_data or {})})
        if snake_data and snake_data.get("total", 0) > 0:
            for item in snake_data.get("items", []):
                uuid_val = item.get("uuid")
                if uuid_val:
                    red_res = ooredoo_redeem_power_snake(msisdn, user, uuid_val)
                    if red_res.get("success"):
                        reward_val = red_res.get('reward', '1 GB')
                        validity_val = red_res.get('validity', '3')
                        return f"✅ تم تفعيل إنترنت صالح لمدة {validity_val} أيام\n📦 حجم الإنترنت: {reward_val}"

        if purchase_ok:
            return "✅ تم تفعيل إنترنت صالح لمدة 3 أيام\n📦 حجم الإنترنت: 1 GB"

        return "❌ لم يتم تفعيل الإنترنت، لم تُؤكد أوريدو العملية.\nلم يتم احتساب هذه المحاولة. يرجى المحاولة لاحقاً."
    except Exception as e:
        print(f"[BUNDLE] exception: {e!r}")
        return "❌ حدث خطأ، يرجى إعادة المحاولة لاحقا."

def is_valid_ooredoo_number(text):
    if not text: return False
    text = re.sub(r'[\s\(\)\-]', '', text.strip())
    return bool(re.match(r'^05\d{8}$', text))

# ══════════════════════════════════════════════════════════════════
#  نظام الإحالة
# ══════════════════════════════════════════════════════════════════
REFERRALS_FILE = "bot_referrals.json"
REFERRAL_REQUIRED = 1  # عدد الإحالات الناجحة المطلوبة لتفعيل الإنترنت
referrals_lock = threading.RLock()
referrals_data = {"referred_by": {}, "successful": {}, "credited_msisdns": []}
_bot_username = None

def load_referrals():
    global referrals_data
    with referrals_lock:
        if os.path.exists(REFERRALS_FILE):
            try:
                with open(REFERRALS_FILE, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                referrals_data = {
                    "referred_by": {str(k): str(v) for k, v in d.get("referred_by", {}).items()},
                    "successful": {str(k): [str(x) for x in v] for k, v in d.get("successful", {}).items()},
                    "credited_msisdns": list(d.get("credited_msisdns", [])),
                }
            except Exception as e:
                print(f"Referrals load error: {e}")

def save_referrals():
    with referrals_lock:
        try:
            with open(REFERRALS_FILE, 'w', encoding='utf-8') as f:
                json.dump(referrals_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Referrals save error: {e}")

def is_referral_enabled():
    with settings_lock:
        return bool(bot_settings.get("referral_enabled", True))

def set_referral_enabled(enabled):
    with settings_lock:
        bot_settings["referral_enabled"] = bool(enabled)
        save_settings()

def is_known_user(uid):
    with settings_lock:
        return uid in known_users

def get_bot_username():
    global _bot_username
    if not _bot_username:
        _bot_username = bot.get_me().username
    return _bot_username

def referral_link(uid):
    return f"https://t.me/{get_bot_username()}?start=ref_{uid}"

def successful_referrals_count(uid):
    with referrals_lock:
        return len(referrals_data["successful"].get(str(uid), []))

def has_unlocked(uid):
    if is_admin(int(uid)) or not is_referral_enabled():
        return True
    return successful_referrals_count(uid) >= REFERRAL_REQUIRED

def parse_referrer(text):
    m = re.match(r'/start\s+ref_(\d+)', (text or "").strip())
    return int(m.group(1)) if m else None

def register_referral_start(invitee, referrer):
    """يُستدعى عند /start ref_X لمستخدم جديد فقط."""
    if invitee == referrer or not is_known_user(referrer):
        return False
    with referrals_lock:
        if str(invitee) in referrals_data["referred_by"]:
            return False
        referrals_data["referred_by"][str(invitee)] = str(referrer)
        save_referrals()
    return True

def credit_referral_on_login(invitee, msisdn):
    """يُستدعى بعد نجاح تسجيل الدخول. يرجع معرّف المُحيل إن حُسبت الإحالة."""
    with referrals_lock:
        referrer = referrals_data["referred_by"].get(str(invitee))
        if not referrer or msisdn in referrals_data["credited_msisdns"]:
            return None
        referrals_data["referred_by"].pop(str(invitee), None)
        referrals_data["credited_msisdns"].append(msisdn)
        lst = referrals_data["successful"].setdefault(referrer, [])
        if str(invitee) not in lst:
            lst.append(str(invitee))
        save_referrals()
        return referrer

def referral_text(uid):
    if not is_referral_enabled():
        return "👥 نظام الإحالة\n\n✅ نظام الإحالة متوقف حالياً، يمكنك استخدام البوت بشكل طبيعي."
    cnt = successful_referrals_count(uid)
    if has_unlocked(uid):
        status = "✅ تم فتح البوت لك، يمكنك الآن تفعيل الإنترنت."
    else:
        status = (f"🔒 لاستخدام البوت يجب أن تُحيل {REFERRAL_REQUIRED} شخصاً إحالة ناجحة.\n"
                  f"إحالاتك الناجحة: {cnt}/{REFERRAL_REQUIRED}")
    return (
        "👥 نظام الإحالة\n\n"
        f"{status}\n\n"
        "🔗 رابط إحالتك:\n"
        f"{referral_link(uid)}\n\n"
        "تُحتسب الإحالة ناجحة عندما يدخل المدعو عبر رابطك ويسجّل دخوله برقم هاتفه بنجاح."
    )

def referral_markup(uid):
    m = InlineKeyboardMarkup(row_width=1)
    share_text = "جرّب بوت تفعيل الإنترنت بسهولة 🚀"
    url = (f"https://t.me/share/url?url={urllib.parse.quote(referral_link(uid))}"
           f"&text={urllib.parse.quote(share_text)}")
    m.add(InlineKeyboardButton("📤 مشاركة الرابط", url=url))
    m.add(InlineKeyboardButton("✅ تحقق من الإحالة", callback_data="ref_check"))
    return m

def send_referral_gate(chat_id):
    if has_unlocked(chat_id):
        return
    bot.send_message(chat_id, referral_text(chat_id), reply_markup=referral_markup(chat_id))

def phone_entry_allowed(uid):
    """لا يُسمح بإرسال الرقم إلا لمن أكمل الإحالة المطلوبة،
    أو للقادم عبر رابط إحالة (لازم يسجّل دخوله حتى تُحسب الإحالة لصاحبه)."""
    if has_unlocked(uid):
        return True
    with referrals_lock:
        return str(uid) in referrals_data["referred_by"]

def get_main_menu_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("⚡ تفعيل إنترنت", callback_data="menu_activate_1gb"),
        InlineKeyboardButton("👥 الإحالة", callback_data="menu_referral"),
        InlineKeyboardButton("🔄 تسجيل الدخول من جديد", callback_data="menu_relogin")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    executor.submit(handle_start_async, message)

def handle_start_async(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not is_admin(user_id) and not is_bot_enabled():
        bot.send_message(chat_id, BOT_STOPPED_MSG)
        return
    if is_blocked(user_id):
        bot.send_message(chat_id, BANNED_MSG)
        return
    is_new = (not is_known_user(chat_id)) and ooredoo_get_user(chat_id) is None
    register_user(chat_id)
    if is_new:
        ref = parse_referrer(message.text)
        if ref:
            register_referral_start(chat_id, ref)

    if not check_user_subscription(user_id):
        bot.send_message(
            chat_id,
            "مرحبًا بك! 💜\n"
            "بوت لتفعيل الإنترنت بسهولة وسرعة 🚀\n"
            "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱.",
            reply_markup=get_subscription_markup()
        )
        return

    user = ooredoo_get_user(chat_id)
    if user:
        bot.send_message(
            chat_id, 
            f"مرحباً بك مجدداً 🚀\n\nحسابك المرتبط حالياً: ({user.get('msisdn')})\nاختر ما تحتاجه من القائمة أدناه:", 
            reply_markup=get_main_menu_keyboard()
        )
    else:
        ooredoo_clear_session(chat_id)
        ooredoo_set_session(chat_id, {"state": "awaiting_phone"})
        bot.send_message(
            chat_id, 
            "مرحبًا بك! 💜\n"
            "بوت لتفعيل الإنترنت بسهولة وسرعة 🚀\n"
            "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱."
        )

    send_referral_gate(chat_id)

# ══════════════════════════════════════════════════════════════════
#  لوحة الأدمن: /admin
# ══════════════════════════════════════════════════════════════════
ALL_CONTENT_TYPES = ['text', 'photo', 'video', 'document', 'audio', 'voice',
                     'animation', 'sticker', 'video_note', 'contact', 'location', 'poll']

def is_admin(uid):
    return uid in ADMIN_IDS

def admin_set_state(uid, state, ttl=600):
    ooredoo_store.set(f"admin:state:{uid}", state, ex=ttl)

def admin_get_state(uid):
    return ooredoo_store.get(f"admin:state:{uid}")

def admin_clear_state(uid):
    ooredoo_store.delete(f"admin:state:{uid}")

def admin_main_text():
    total = len(get_all_user_ids())
    return (
        "🛠 لوحة تحكم الأدمن\n\n"
        f"📢 قناة النشر: {get_notify_channel()}\n"
        f"🔒 قنوات الاشتراك الإجباري: {len(get_force_channels())}\n"
        f"🔢 الحد الأقصى للتفعيل: {get_max_activations()} كل 24 ساعة\n"
        f"⏱ الفاصل بين كل تفعيل: {format_duration(get_activation_cooldown())}\n"
        f"🤖 حالة البوت: {'🟢 يعمل' if is_bot_enabled() else '🔴 متوقف'}\n"
        f"👥 نظام الإحالة: {'🟢 يعمل' if is_referral_enabled() else '🔴 متوقف'}\n"
        f"👥 عدد المستخدمين: {total}"
    )

def admin_main_markup():
    m = InlineKeyboardMarkup(row_width=1)
    m.add(
        InlineKeyboardButton("🔴 إيقاف البوت" if is_bot_enabled() else "🟢 تشغيل البوت", callback_data="adm_toggle"),
        InlineKeyboardButton("👥 الإحالة: " + ("🔴 إيقاف" if is_referral_enabled() else "🟢 تشغيل"), callback_data="adm_reftoggle"),
        InlineKeyboardButton("📢 تعديل قناة النشر", callback_data="adm_notify"),
        InlineKeyboardButton("🔒 الاشتراك الإجباري", callback_data="adm_force"),
        InlineKeyboardButton("🔢 تغيير الحد الأقصى", callback_data="adm_limit"),
        InlineKeyboardButton("⏱ الوقت بين كل تفعيل", callback_data="adm_cd"),
        InlineKeyboardButton("📣 الإذاعة", callback_data="adm_bc"),
        InlineKeyboardButton("🚫 حظر مستخدم", callback_data="adm_ban"),
        InlineKeyboardButton("🖼 صورة بعد التفعيل", callback_data="adm_img"),
    )
    return m

def admin_cooldown_markup():
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("1 دقيقة", callback_data="adm_cdset:60"),
        InlineKeyboardButton("5 دقائق", callback_data="adm_cdset:300"),
        InlineKeyboardButton("30 دقيقة", callback_data="adm_cdset:1800"),
        InlineKeyboardButton("ساعة", callback_data="adm_cdset:3600"),
        InlineKeyboardButton("3 ساعات", callback_data="adm_cdset:10800"),
        InlineKeyboardButton("6 ساعات", callback_data="adm_cdset:21600"),
    )
    m.add(InlineKeyboardButton("✏️ وقت مخصص", callback_data="adm_cdcustom"))
    m.add(InlineKeyboardButton("🚫 تعطيل الفاصل", callback_data="adm_cdset:0"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="adm_home"))
    return m

def admin_cooldown_text():
    return (
        "⏱ الوقت بين كل تفعيل\n\n"
        f"الحالي: {format_duration(get_activation_cooldown())}\n\n"
        "هو المدة التي يجب أن ينتظرها كل رقم بين تفعيل والذي يليه.\n"
        "اختر مدة جاهزة أو أرسل وقتاً مخصصاً."
    )

def admin_ban_text():
    return (
        "🚫 حظر المستخدمين\n\n"
        f"عدد المحظورين: {len(get_banned_users())}\n\n"
        "الحظر يمنع المستخدم من استخدام البوت.\n"
        "اضغط على المعرّف لفك حظره، أو أضف مستخدماً جديداً."
    )

def admin_ban_markup():
    m = InlineKeyboardMarkup(row_width=1)
    for uid in get_banned_users():
        m.add(InlineKeyboardButton(f"✅ فك حظر {uid}", callback_data=f"adm_unban:{uid}"))
    m.add(InlineKeyboardButton("➕ حظر مستخدم", callback_data="adm_banadd"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="adm_home"))
    return m

def admin_img_text():
    has = bool(get_success_image())
    return (
        "🖼 الصورة بعد التفعيل الناجح\n\n"
        f"الحالة: {'✅ مضبوطة' if has else '❌ غير مضبوطة'}\n\n"
        "عند نجاح التفعيل ستُرسل هذه الصورة للمستخدم مع رسالة النجاح.\n"
        "أرسل صورة الآن لتعيينها، أو احذف الصورة الحالية.\n"
        "للإلغاء: /cancel"
    )

def admin_img_markup():
    m = InlineKeyboardMarkup(row_width=1)
    if get_success_image():
        m.add(InlineKeyboardButton("🗑 حذف الصورة", callback_data="adm_imgdel"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="adm_home"))
    return m

def admin_back_markup():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="adm_home"))
    return m

def admin_force_text():
    chans = get_force_channels()
    if not chans:
        return "🔒 الاشتراك الإجباري\n\nلا توجد قنوات حالياً (الاشتراك معطّل)."
    lines = "\n".join(f"{i}. {c['channel']}" for i, c in enumerate(chans, 1))
    return f"🔒 قنوات الاشتراك الإجباري:\n\n{lines}"

def admin_force_markup():
    m = InlineKeyboardMarkup(row_width=1)
    for i, c in enumerate(get_force_channels()):
        m.add(InlineKeyboardButton(f"🗑 حذف {c['channel']}", callback_data=f"adm_fdel:{i}"))
    m.add(InlineKeyboardButton("➕ إضافة قناة", callback_data="adm_fadd"))
    m.add(InlineKeyboardButton("🔙 رجوع", callback_data="adm_home"))
    return m

def validate_channel(ch, need_post=False):
    """يتحقق أن البوت يستطيع الوصول للقناة وأنه مشرف فيها. يرجع (ok, title_or_error)."""
    try:
        chat = bot.get_chat(ch)
    except Exception:
        return False, "تعذر الوصول للقناة. تأكد من صحة المعرف وأن البوت مضاف إليها."
    try:
        member = bot.get_chat_member(chat.id, bot.get_me().id)
    except Exception:
        return False, "تعذر التحقق من صلاحيات البوت في القناة."
    if member.status not in ('administrator', 'creator'):
        return False, "البوت ليس مشرفاً في هذه القناة. أضفه كمشرف ثم أعد المحاولة."
    if need_post and member.status == 'administrator' and getattr(member, 'can_post_messages', None) is False:
        return False, "البوت لا يملك صلاحية نشر الرسائل في القناة."
    return True, (chat.title or str(ch))

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if not is_admin(message.from_user.id) or message.chat.type != 'private':
        return
    admin_clear_state(message.from_user.id)
    bot.send_message(message.chat.id, admin_main_text(), reply_markup=admin_main_markup())

def admin_state_filter(m):
    try:
        if not is_admin(m.from_user.id) or m.chat.type != 'private':
            return False
        if not admin_get_state(m.from_user.id):
            return False
        t = m.text or ""
        return not (t.startswith("/") and t.split()[0].lower() != "/cancel")
    except Exception:
        return False

@bot.message_handler(func=admin_state_filter, content_types=ALL_CONTENT_TYPES)
def admin_state_handler(message):
    executor.submit(handle_admin_state_async, message)

def handle_admin_state_async(message):
    uid = message.from_user.id
    chat_id = message.chat.id
    state = admin_get_state(uid)
    text = (message.text or "").strip()

    if text.lower() == "/cancel":
        admin_clear_state(uid)
        bot.send_message(chat_id, "❎ تم الإلغاء.\n\n" + admin_main_text(), reply_markup=admin_main_markup())
        return

    # ── تعديل قناة النشر ──
    if state == "notify":
        parsed = parse_channel_input(text)
        if not parsed:
            bot.send_message(chat_id, "❌ صيغة غير صحيحة. أرسل @username أو رابط القناة أو المعرف الرقمي (-100...).\nللإلغاء: /cancel")
            return
        ch = parsed[0]
        ok, info = validate_channel(ch, need_post=True)
        if not ok:
            bot.send_message(chat_id, f"❌ {info}\nللإلغاء: /cancel")
            return
        set_notify_channel(ch)
        admin_clear_state(uid)
        bot.send_message(chat_id, f"✅ تم تحديث قناة النشر إلى: {info} ({ch})", reply_markup=admin_main_markup())
        return

    # ── إضافة قناة اشتراك إجباري ──
    if state == "force_add":
        parsed = parse_channel_input(text)
        if not parsed:
            bot.send_message(chat_id, "❌ صيغة غير صحيحة. أرسل @username أو رابط القناة أو المعرف الرقمي (-100...).\nللإلغاء: /cancel")
            return
        ch, link = parsed
        if any(str(c["channel"]) == str(ch) for c in get_force_channels()):
            bot.send_message(chat_id, "⚠️ هذه القناة مضافة مسبقاً.\nللإلغاء: /cancel")
            return
        ok, info = validate_channel(ch)
        if not ok:
            bot.send_message(chat_id, f"❌ {info}\nللإلغاء: /cancel")
            return
        if link is None:
            # قناة خاصة بمعرف رقمي: نحتاج رابط دعوة للزر
            ooredoo_store.set(f"admin:pending_ch:{uid}", ch, ex=600)
            admin_set_state(uid, "force_add_link")
            bot.send_message(chat_id, f"✅ تم التحقق من: {info}\n\n🔗 أرسل الآن رابط الدعوة الخاص بالقناة (https://t.me/...):")
            return
        add_force_channel(ch, link)
        admin_clear_state(uid)
        bot.send_message(chat_id, f"✅ تمت إضافة القناة: {info} ({ch})\n\n" + admin_force_text(), reply_markup=admin_force_markup())
        return

    if state == "force_add_link":
        ch = ooredoo_store.get(f"admin:pending_ch:{uid}")
        if not ch:
            admin_clear_state(uid)
            bot.send_message(chat_id, "⌛ انتهت الجلسة. ابدأ من جديد.", reply_markup=admin_main_markup())
            return
        if not re.match(r'^https://t\.me/\S+$', text):
            bot.send_message(chat_id, "❌ الرابط يجب أن يبدأ بـ https://t.me/\nللإلغاء: /cancel")
            return
        add_force_channel(ch, text)
        ooredoo_store.delete(f"admin:pending_ch:{uid}")
        admin_clear_state(uid)
        bot.send_message(chat_id, "✅ تمت إضافة القناة.\n\n" + admin_force_text(), reply_markup=admin_force_markup())
        return

    # ── تغيير الحد الأقصى ──
    if state == "limit":
        if not text.isdigit() or not (1 <= int(text) <= 1000):
            bot.send_message(chat_id, "❌ أرسل رقماً صحيحاً بين 1 و 1000.\nللإلغاء: /cancel")
            return
        set_max_activations(int(text))
        admin_clear_state(uid)
        bot.send_message(chat_id, f"✅ تم تغيير الحد الأقصى إلى {int(text)} تفعيل لكل رقم خلال 24 ساعة.", reply_markup=admin_main_markup())
        return

    # ── الوقت بين كل تفعيل (مخصص) ──
    if state == "cooldown":
        secs = parse_duration(text)
        if secs is None or secs > 7 * 86400:
            bot.send_message(chat_id, "❌ صيغة غير صحيحة.\nأمثلة: 30 (دقائق) ، 45s ، 10m ، 2h ، أو 0 للتعطيل.\nللإلغاء: /cancel")
            return
        set_activation_cooldown(secs)
        admin_clear_state(uid)
        bot.send_message(chat_id, f"✅ الفاصل بين كل تفعيل الآن: {format_duration(secs)}", reply_markup=admin_main_markup())
        return

    # ── حظر مستخدم ──
    if state == "ban_add":
        target = None
        if getattr(message, "forward_from", None):
            target = message.forward_from.id
        elif text.isdigit():
            target = int(text)
        if target is None:
            bot.send_message(chat_id, "❌ أرسل معرّفاً رقمياً (ID) صحيحاً أو أعد توجيه رسالة من المستخدم.\nللإلغاء: /cancel")
            return
        if is_admin(target):
            bot.send_message(chat_id, "⛔ لا يمكن حظر الأدمن.\nللإلغاء: /cancel")
            return
        ban_user(target)
        admin_clear_state(uid)
        bot.send_message(chat_id, f"🚫 تم حظر المستخدم {target}.\n\n" + admin_ban_text(), reply_markup=admin_ban_markup())
        return

    # ── الصورة بعد التفعيل الناجح ──
    if state == "img_wait":
        if message.content_type != 'photo' or not message.photo:
            bot.send_message(chat_id, "❌ أرسل صورة (وليس نصاً أو ملفاً).\nللإلغاء: /cancel")
            return
        set_success_image(message.photo[-1].file_id)
        admin_clear_state(uid)
        bot.send_message(chat_id, "✅ تم حفظ الصورة. ستُرسل للمستخدمين بعد كل تفعيل ناجح.", reply_markup=admin_main_markup())
        return

    # ── الإذاعة: استقبال الرسالة ثم طلب التأكيد ──
    if state == "bc_wait":
        ooredoo_store.set(f"admin:bc:{uid}", json.dumps({"chat_id": chat_id, "message_id": message.message_id}), ex=900)
        admin_clear_state(uid)
        try:
            bot.copy_message(chat_id, chat_id, message.message_id)
        except Exception:
            pass
        m = InlineKeyboardMarkup(row_width=2)
        m.add(
            InlineKeyboardButton("✅ إرسال", callback_data="adm_bcgo"),
            InlineKeyboardButton("❌ إلغاء", callback_data="adm_home"),
        )
        bot.send_message(chat_id, f"👆 هذه معاينة الرسالة.\nسيتم إرسالها إلى {len(get_all_user_ids())} مستخدم. هل تؤكد؟", reply_markup=m)
        return

def _broadcast_send_one(uid, src_chat_id, src_msg_id):
    try:
        bot.copy_message(uid, src_chat_id, src_msg_id)
        return True
    except ApiTelegramException as e:
        if e.error_code == 429:
            try:
                wait = int((e.result_json or {}).get("parameters", {}).get("retry_after", 5))
            except Exception:
                wait = 5
            time.sleep(min(wait, 30) + 1)
            try:
                bot.copy_message(uid, src_chat_id, src_msg_id)
                return True
            except Exception:
                return False
        return False
    except Exception:
        return False

def run_broadcast(admin_chat_id, src_chat_id, src_msg_id, status_msg_id):
    targets = sorted(u for u in get_all_user_ids() if not is_blocked(u))
    total = len(targets)
    ok = fail = 0
    for i, uid in enumerate(targets, 1):
        if _broadcast_send_one(uid, src_chat_id, src_msg_id):
            ok += 1
        else:
            fail += 1
        time.sleep(0.05)  # ~20 رسالة/ثانية أقل من حد تيليجرام
        if i % 50 == 0:
            try:
                bot.edit_message_text(f"📣 جاري الإرسال... {i}/{total}", admin_chat_id, status_msg_id)
            except Exception:
                pass
    report = f"✅ انتهت الإذاعة\n\n👥 الإجمالي: {total}\n✔️ نجح: {ok}\n✖️ فشل: {fail}"
    try:
        bot.edit_message_text(report, admin_chat_id, status_msg_id, reply_markup=admin_main_markup())
    except Exception:
        bot.send_message(admin_chat_id, report, reply_markup=admin_main_markup())

def handle_admin_callback(call):
    uid = call.from_user.id
    if not is_admin(uid):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    chat_id = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    bot.answer_callback_query(call.id)

    def show(text, markup):
        try:
            bot.edit_message_text(text, chat_id, mid, reply_markup=markup)
        except Exception as e:
            if "not modified" not in str(e):
                bot.send_message(chat_id, text, reply_markup=markup)

    if data == "adm_home":
        admin_clear_state(uid)
        show(admin_main_text(), admin_main_markup())

    elif data == "adm_toggle":
        set_bot_enabled(not is_bot_enabled())
        state_txt = "🟢 تم تشغيل البوت." if is_bot_enabled() else "🔴 تم إيقاف البوت للمستخدمين."
        show(state_txt + "\n\n" + admin_main_text(), admin_main_markup())

    elif data == "adm_reftoggle":
        set_referral_enabled(not is_referral_enabled())
        state_txt = ("🟢 تم تشغيل نظام الإحالة." if is_referral_enabled()
                     else "🔴 تم إيقاف نظام الإحالة (البوت مفتوح للجميع).")
        show(state_txt + "\n\n" + admin_main_text(), admin_main_markup())

    elif data == "adm_notify":
        admin_set_state(uid, "notify")
        show(f"📢 قناة النشر الحالية: {get_notify_channel()}\n\n"
             "أرسل القناة الجديدة: @username أو رابط القناة أو المعرف الرقمي (-100...).\n"
             "⚠️ يجب أن يكون البوت مشرفاً في القناة مع صلاحية النشر.\n"
             "للإلغاء: /cancel", admin_back_markup())

    elif data == "adm_force":
        admin_clear_state(uid)
        show(admin_force_text(), admin_force_markup())

    elif data == "adm_fadd":
        admin_set_state(uid, "force_add")
        show("➕ أرسل القناة المراد إضافتها: @username أو رابط القناة أو المعرف الرقمي (-100...).\n"
             "⚠️ يجب أن يكون البوت مشرفاً فيها ليتمكن من فحص الاشتراك.\n"
             "للإلغاء: /cancel", admin_back_markup())

    elif data.startswith("adm_fdel:"):
        try:
            idx = int(data.split(":", 1)[1])
        except ValueError:
            return
        removed = remove_force_channel(idx)
        prefix = f"🗑 تم حذف {removed['channel']}\n\n" if removed else ""
        show(prefix + admin_force_text(), admin_force_markup())

    elif data == "adm_limit":
        admin_set_state(uid, "limit")
        show(f"🔢 الحد الأقصى الحالي: {get_max_activations()} تفعيل لكل رقم خلال 24 ساعة.\n\n"
             "أرسل الرقم الجديد (من 1 إلى 1000).\nللإلغاء: /cancel", admin_back_markup())

    elif data == "adm_cd":
        admin_clear_state(uid)
        show(admin_cooldown_text(), admin_cooldown_markup())

    elif data == "adm_cdcustom":
        admin_set_state(uid, "cooldown")
        show(f"✏️ الفاصل الحالي: {format_duration(get_activation_cooldown())}\n\n"
             "أرسل المدة الجديدة:\n"
             "• رقم فقط = دقائق (مثال: 30)\n"
             "• 45s = ثواني ، 10m = دقائق ، 2h = ساعات\n"
             "• 0 = تعطيل الفاصل\nللإلغاء: /cancel", admin_back_markup())

    elif data.startswith("adm_cdset:"):
        try:
            secs = int(data.split(":", 1)[1])
        except ValueError:
            return
        set_activation_cooldown(secs)
        show(admin_cooldown_text(), admin_cooldown_markup())

    elif data == "adm_ban":
        admin_clear_state(uid)
        show(admin_ban_text(), admin_ban_markup())

    elif data == "adm_banadd":
        admin_set_state(uid, "ban_add")
        show("🚫 أرسل معرّف المستخدم (ID) المراد حظره، أو أعد توجيه رسالة منه.\n"
             "للإلغاء: /cancel", admin_back_markup())

    elif data.startswith("adm_unban:"):
        try:
            target = int(data.split(":", 1)[1])
        except ValueError:
            return
        unban_user(target)
        show(f"✅ تم فك حظر {target}.\n\n" + admin_ban_text(), admin_ban_markup())

    elif data == "adm_img":
        admin_set_state(uid, "img_wait")
        show(admin_img_text(), admin_img_markup())

    elif data == "adm_imgdel":
        admin_clear_state(uid)
        set_success_image(None)
        show("🗑 تم حذف الصورة.\n\n" + admin_img_text(), admin_img_markup())

    elif data == "adm_bc":
        admin_set_state(uid, "bc_wait", ttl=900)
        show("📣 الإذاعة\n\nأرسل الرسالة التي تريد إذاعتها لجميع المستخدمين "
             "(نص، صورة، فيديو، ملف...).\nللإلغاء: /cancel", admin_back_markup())

    elif data == "adm_bcgo":
        raw = ooredoo_store.get(f"admin:bc:{uid}")
        if not raw:
            show("⌛ انتهت صلاحية الرسالة. ابدأ الإذاعة من جديد.", admin_main_markup())
            return
        ooredoo_store.delete(f"admin:bc:{uid}")
        info = json.loads(raw)
        show("📣 بدأت الإذاعة...", None)
        executor.submit(run_broadcast, chat_id, info["chat_id"], info["message_id"], mid)

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_messages(message):
    executor.submit(handle_messages_async, message)

def handle_messages_async(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not message.text: return
    if not is_admin(user_id) and not is_bot_enabled():
        bot.send_message(chat_id, BOT_STOPPED_MSG)
        return
    if is_blocked(user_id):
        bot.send_message(chat_id, BANNED_MSG)
        return
    register_user(chat_id)
    text = message.text.strip()

    if not check_user_subscription(user_id):
        bot.send_message(
            chat_id,
            "مرحبًا بك! 💜\n"
            "بوت لتفعيل الإنترنت بسهولة وسرعة 🚀\n"
            "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱.",
            reply_markup=get_subscription_markup()
        )
        return

    osess = ooredoo_get_session(chat_id)
    ostate = osess.get("state", "")

    if ostate in ("awaiting_phone", "awaiting_otp") and not phone_entry_allowed(chat_id):
        bot.send_message(
            chat_id,
            f"🔒 لا يمكنك إرسال رقمك قبل إكمال الإحالة المطلوبة.\n"
            f"إحالاتك الناجحة: {successful_referrals_count(chat_id)}/{REFERRAL_REQUIRED}\n"
            "شارك رابط إحالتك، وبعد أن يسجّل المدعو دخوله بنجاح سيُفتح البوت لك.",
            reply_markup=referral_markup(chat_id)
        )
        return
    
    if ostate == "awaiting_phone":
        digits = "".join(c for c in text if c.isdigit())
        if not is_valid_ooredoo_number(text):
            bot.send_message(chat_id, "❌ رقم غير صحيح. أرسل رقم أوريدو (05XXXXXXXX)")
            return
        msisdn = "213" + digits[1:]
        
        cooldown_key = f"otp_cooldown:{msisdn}"
        last_sent = ooredoo_store.get(cooldown_key)
        if last_sent:
            elapsed = time.time() - float(last_sent)
            if elapsed < 40:
                remaining = int(40 - elapsed)
                bot.send_message(chat_id, f"⚠️ يرجى الانتظار {remaining} ثانية قبل طلب رمز تحقق جديد.")
                return

        ooredoo_set_session(chat_id, {"state": "sending_otp", "msisdn": msisdn})
        bot.send_message(chat_id, "⏳ جاري إرسال رمز التحقق...")
        device = ooredoo_get_or_create_device(chat_id)
        res = ooredoo_send_otp(msisdn, device)
        if not res:
            bot.send_message(chat_id, "❌ تعذر إرسال رمز التحقق حالياً.\nأعد إرسال رقمك للمحاولة مرة أخرى.")
            ooredoo_set_session(chat_id, {"state": "awaiting_phone"})
            return
        
        ooredoo_store.set(cooldown_key, str(time.time()), ex=40)

        ooredoo_set_session(chat_id, {
            "state": "awaiting_otp",
            "msisdn": msisdn,
            "proxy_host": res["proxy"]["host"] if res.get("proxy") else "",
            "proxy_user": res["proxy"]["userpass"] if res.get("proxy") else ""
        })
        bot.send_message(chat_id, "📲 تم إرسال رمز التحقق بنجاح.\n\n📝 أدخل الرمز المكون من 6 أرقام:")
        return

    if ostate == "awaiting_otp":
        if not text.isdigit() or len(text) != 6:
            bot.send_message(chat_id, "❌ الرمز يجب أن يكون 6 أرقام صحيحة.")
            return
        msisdn = osess.get("msisdn")
        proxy = {"host": osess.get("proxy_host", ""), "userpass": osess.get("proxy_user", "")}
        device = ooredoo_get_or_create_device(chat_id)
        vm = bot.send_message(chat_id, "🔐 جاري التحقق من الرمز...")
        res = ooredoo_verify_otp(msisdn, text, proxy, device)
        if vm:
            try: bot.delete_message(chat_id, vm.message_id)
            except: pass
        if res == "wrong_otp":
            bot.send_message(chat_id, "❌ رمز التحقق خاطئ، يرجى المحاولة مرة أخرى.")
            return
        if not res:
            bot.send_message(chat_id, "❌ تعذر التحقق من الرمز بسبب ضعف الاتصال بخدمة أوريدو.\nأرسل رقمك من جديد لطلب رمز جديد.")
            ooredoo_clear_session(chat_id)
            return
        new_user = {"msisdn": msisdn, "operator": "ooredoo", "created_at": int(time.time())}
        new_user.update(res)
        ooredoo_save_user(chat_id, new_user)
        referrer = credit_referral_on_login(chat_id, msisdn)
        if referrer:
            try:
                notify = f"🎉 نجحت إحالة جديدة عبر رابطك!\nإحالاتك الناجحة: {successful_referrals_count(referrer)}/{REFERRAL_REQUIRED}"
                if has_unlocked(referrer):
                    notify += "\n✅ تم فتح البوت لك."
                bot.send_message(int(referrer), notify)
            except Exception as e:
                print(f"Referral notify error: {e}")
        ooredoo_clear_session(chat_id)
        bot.send_message(chat_id, "✅ تم تسجيل الدخول وربط الحساب بنجاح!", reply_markup=get_main_menu_keyboard())
        return

    bot.send_message(
        chat_id, 
        "مرحبًا بك! 💜\n"
        "بوت لتفعيل الإنترنت بسهولة وسرعة 🚀\n"
        "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱.", 
        reply_markup=get_main_menu_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    executor.submit(handle_callbacks_async, call)

def handle_callbacks_async(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    data = call.data

    if data.startswith("adm_"):
        handle_admin_callback(call)
        return

    if is_blocked(user_id):
        bot.answer_callback_query(call.id, BANNED_MSG, show_alert=True)
        return

    if not is_admin(user_id) and not is_bot_enabled():
        bot.answer_callback_query(call.id, BOT_STOPPED_MSG, show_alert=True)
        return

    if data == "check_sub":
        if check_user_subscription(user_id):
            bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!", show_alert=True)
            try: bot.delete_message(chat_id, call.message.message_id)
            except: pass
            user = ooredoo_get_user(chat_id)
            if user:
                bot.send_message(chat_id, f"مرحباً بك مجدداً 🚀\nرقمك المرتبط: ({user.get('msisdn')})", reply_markup=get_main_menu_keyboard())
            else:
                ooredoo_clear_session(chat_id)
                ooredoo_set_session(chat_id, {"state": "awaiting_phone"})
                bot.send_message(
                    chat_id, 
                    "مرحبًا بك! 💜\n"
                    "بوت لتفعيل الإنترنت بسهولة وسرعة 🚀\n"
                    "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱."
                )
            send_referral_gate(chat_id)
        else:
            bot.answer_callback_query(call.id, "❌ يرجى التأكد من الاشتراك في القنوات أولاً!", show_alert=True)
        return

    if data == "ref_check":
        if has_unlocked(chat_id):
            bot.answer_callback_query(call.id, "✅ تم فتح البوت لك!", show_alert=True)
            bot.send_message(chat_id, "🎉 يمكنك الآن استخدام البوت.", reply_markup=get_main_menu_keyboard())
        else:
            bot.answer_callback_query(
                call.id,
                f"🔒 إحالاتك الناجحة: {successful_referrals_count(chat_id)}/{REFERRAL_REQUIRED}",
                show_alert=True
            )
        return

    if data == "menu_referral":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, referral_text(chat_id), reply_markup=referral_markup(chat_id))
        return

    user = ooredoo_get_user(chat_id)
    if data == "menu_relogin":
        ooredoo_delete_user(chat_id)
        ooredoo_clear_session(chat_id)
        ooredoo_set_session(chat_id, {"state": "awaiting_phone"})
        bot.answer_callback_query(call.id, "🔄 تم تسجيل الخروج.")
        bot.edit_message_text(
            "مرحبًا بك! 💜\n"
            "بوت لتفعيل الإنترنت بسهولة وسرعة 🚀\n"
            "أرسل رقم هاتفك (10 أرقام) لبدء التفعيل 📱.", 
            chat_id, 
            call.message.message_id
        )
        return

    if not user:
        bot.answer_callback_query(call.id, "❌ انتهت الجلسة، أرسل /start", show_alert=True)
        return

    msisdn = user.get("msisdn")

    if data == "menu_activate_1gb" and not has_unlocked(chat_id):
        bot.answer_callback_query(call.id, "🔒 يجب إحالة شخص ناجحة أولاً.", show_alert=True)
        bot.send_message(chat_id, referral_text(chat_id), reply_markup=referral_markup(chat_id))
        return

    if data == "menu_activate_1gb":
        allowed, info = check_and_record_activation(msisdn)
        if not allowed:
            if info.get("reason") == "cooldown":
                wait = format_duration(info["remaining"])
                bot.answer_callback_query(call.id, f"⏳ يرجى الانتظار {wait} قبل التفعيل التالي.", show_alert=True)
                bot.send_message(chat_id, f"⏳ يجب الانتظار {wait} قبل تفعيل جديد.", reply_markup=get_main_menu_keyboard())
                return
            bot.answer_callback_query(call.id, f"⚠️ عذراً، هذا الرقم استنفد الحد الأقصى ({get_max_activations()}) خلال 24 ساعة!", show_alert=True)
            bot.send_message(chat_id, f"⚠️ عذراً، هذا الرقم استنفد الحد الأقصى المسموح به ({get_max_activations()}) خلال الـ 24 ساعة الماضية.", reply_markup=get_main_menu_keyboard())
            return

        bot.answer_callback_query(call.id, "⏳ جاري تفعيل إنترنت...")
        vm = bot.send_message(chat_id, "⏳ جاري تفعيل إنترنت... 🚀")
        result_msg = ooredoo_activate_target_bundle(msisdn, user)
        if not str(result_msg).startswith("✅"):
            refund_activation(msisdn)
        try: bot.delete_message(chat_id, vm.message_id)
        except: pass
        img_id = get_success_image() if str(result_msg).startswith("✅") else None
        sent_photo = False
        if img_id:
            try:
                bot.send_photo(chat_id, img_id, caption=result_msg, reply_markup=get_main_menu_keyboard())
                sent_photo = True
            except Exception as e:
                print(f"Success image send error: {e}")
        if not sent_photo:
            bot.send_message(chat_id, f"{result_msg}", reply_markup=get_main_menu_keyboard())
        
        try:
            username = f"@{call.from_user.username}" if call.from_user.username else (call.from_user.first_name or "مستخدم")
            masked_num = mask_msisdn(msisdn)
            notif_text = (
                f"🎉 **عملية تفعيل ناجحة**\n\n"
                f"👤 المستخدم: {username}\n"
                f"📱 الرقم: `{masked_num}`\n"
                f"📦 التفاصيل: {result_msg}\n\n"
                f"⚡ تم عبر 𝐒𝐀𝐋𝐀𝐇-𝐃𝐙 "
            )
            bot.send_message(get_notify_channel(), notif_text, parse_mode='Markdown')
        except Exception as e:
            print(f"Channel notification error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 NEXION Bot2 RUNNING (VERSION 1.5.17 - FIXED & STABLE)...")
    print("=" * 60)
    load_ooredoo_data()
    load_settings()
    load_referrals()
    bot.infinity_polling(timeout=60, long_polling_timeout=30, none_stop=True)
