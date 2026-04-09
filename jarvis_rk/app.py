"""JARVIS AI - Build RK | Created by Ritik Boss"""
import os, ctypes, urllib.parse, urllib.request, subprocess, webbrowser
import json, traceback, pathlib, random, ssl, re
from datetime import datetime
from collections import deque
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
BASE = pathlib.Path(__file__).parent
GEMINI_KEY = "AIzaSyBXr8mm_3auzbbMw1xTEcejLb9vd-LX1iM"
OR_KEY = "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"
_mem, _names = {}, {}

def get_hist(sid):
    if sid not in _mem: _mem[sid] = deque(maxlen=10)
    return _mem[sid]

def detect_lang(text):
    gu = sum(1 for c in text if '\u0A80' <= c <= '\u0AFF')
    hi = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    if gu > 0: return "gu"
    if hi > 0: return "hi"
    return None

def ask_ai(msg, lang, hist, uname=""):
    lm = {"hi":"Hindi","en":"English","gu":"Gujarati","mr":"Marathi"}
    tgt = lm.get(lang,"Hindi")
    sp = ("You are JARVIS RK, a smart AI assistant created by Ritik Boss. "
          + (f"User: {uname}. " if uname else "")
          + f"Reply ONLY in {tgt}. Friendly, helpful. Use Boss. "
          + "If asked who made you: Mujhe Ritik Boss ne banaya hai. "
          + "NEVER repeat input. Max 4 sentences.")
    prompt = sp + "\n\n"
    for h in list(hist)[-4:]: prompt += h["role"].title()+": "+h["msg"]+"\n"
    prompt += "User: "+msg+"\nJARVIS:"
    bg = json.dumps({"contents":[{"role":"user","parts":[{"text":prompt}]}],
                     "generationConfig":{"temperature":0.9,"maxOutputTokens":300}}).encode()
    ctx = ssl.create_default_context()
    for gm in ["gemini-2.0-flash-lite","gemini-2.0-flash","gemini-1.5-flash-8b","gemini-1.5-flash"]:
        try:
            req = urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/{gm}:generateContent?key={GEMINI_KEY}",
                data=bg, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                d = json.loads(r.read().decode())
                txt = d["candidates"][0]["content"]["parts"][0]["text"].strip()
                print(f"[GEMINI:{gm}] {txt[:60]}")
                return txt
        except Exception as e: print(f"[G:{gm}] {e}")
    msgs = [{"role":"system","content":sp}]
    for h in list(hist)[-6:]: msgs.append({"role":h["role"],"content":h["msg"]})
    msgs.append({"role":"user","content":msg})
    for model in ["meta-llama/llama-3.2-3b-instruct:free","microsoft/phi-3-mini-128k-instruct:free"]:
        try:
            b2 = json.dumps({"model":model,"messages":msgs,"max_tokens":300,"temperature":0.9}).encode()
            r2 = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=b2,
                headers={"Authorization":f"Bearer {OR_KEY}","Content-Type":"application/json",
                         "HTTP-Referer":"http://127.0.0.1:8002","X-Title":"JARVIS RK"})
            with urllib.request.urlopen(r2, timeout=12, context=ctx) as r:
                d = json.loads(r.read().decode())
                txt = d["choices"][0]["message"]["content"].strip()
                print(f"[OR] {txt[:60]}")
                return txt
        except Exception as e: print(f"[OR:{model[:12]}] {e}")
    return None

def fallback(msg, lang):
    t = msg.lower(); raw = msg
    greets = ["hello","hi","hey","namaste","kem cho","kaise ho","kese ho","how are you","majama","kem chho"]
    if any(w in t for w in greets):
        return random.choice(["Hello Boss! JARVIS RK ready hai. Kya kar sakta hoon?","Hey Boss! Main hazir hoon. Boliye!","Kya haal hai Boss! Seva mein ready hoon."])
    if any(w in t for w in ["kaun ho","who are you","jarvis kaun","rk kaun","tum kaun","kon chhe"]) or "कौन हो" in raw:
        return "Main JARVIS RK hoon — Ritik Boss ka personal AI assistant! Commands execute karta hoon aur sawaalon ka jawab deta hoon."
    if any(w in t for w in ["kisne banaya","who made","who created","creator","kone banavio"]) or "किसने बनाया" in raw:
        return "Mujhe Ritik Boss ne banaya hai! Main unka personal next-generation AI assistant hoon."
    if any(w in t for w in ["kya kar sakte","what can you do","features","help","madad"]):
        return "Boss, main YouTube/Google/WhatsApp/Chrome khol sakta hoon, apps open/close, volume control, screenshot, time/date, shutdown/restart aur kisi bhi sawaal ka jawab de sakta hoon!"
    if any(w in t for w in ["joke","mazak","funny","hasao"]):
        return random.choice(["Boss joke! Ek programmer ghar aaya: Aaj 99 bugs fix kiye! Patni: Wah! Programmer: Kal 100 naye aa gaye!","Why do programmers prefer dark mode? Light attracts bugs!"])
    if any(w in t for w in ["kahani","story","kissa","sunao"]) or "कहानी" in raw:
        return "Boss, ek kahani! Ek ladka tha jo roz sapne dekhta tha. Log kehte nahi hoga. Lekin usne haar nahi maani, mehnat ki aur ek din safal ho gaya! Moral: Sapne dekho aur mehnat karo!"
    kb = {"python":"Python ek powerful programming language hai jo AI, web development aur automation mein use hoti hai!",
          "java":"Java ek object-oriented language hai. Android apps aur enterprise software mein widely use hota hai.",
          "javascript":"JavaScript web ka king hai! Websites ko interactive banata hai. React, Node.js — JS har jagah hai!",
          "operating system":"Operating system ek system software hai jo computer hardware ko manage karta hai. Windows, Linux, macOS popular OS hain.",
          "artificial intelligence":"AI machines ko intelligent banata hai! Machine Learning, Deep Learning, NLP — sab AI ke parts hain.",
          "machine learning":"Machine Learning AI ka dil hai! Computers data se khud seekhte hain.",
          "computer":"Computer ek electronic device hai jo data process karta hai. CPU, RAM, Storage main components hain.",
          "internet":"Internet ek global network hai! WWW, email, social media — sab internet pe hai.",
          "india":"India ek mahan desh hai! 1.4 billion logon ka desh, duniya ka sabse bada democracy!",
          "cricket":"Cricket India ka dharam hai Boss! Virat Kohli, Rohit Sharma, MS Dhoni — legends!",
          "narendra modi":"Narendra Modi India ke 14ve Prime Minister hain. 2014 se PM hain. Gujarat ke CM bhi rahe hain.",
          "modi":"Narendra Modi India ke Prime Minister hain. BJP ke neta hain. India ko vishwa shakti banana unka sapna hai.",
          "parul university":"Parul University Vadodara, Gujarat mein hai. Engineering, medical, management courses offer karti hai.",
          "vadodara":"Vadodara Gujarat ka ek important sheher hai. Baroda ke naam se bhi jaana jaata hai.",
          "gujarat":"Gujarat India ka vibrant state hai! Business capital, garba dance, dhokla — culture ke liye famous!",
          "exam":"Exam tips Boss! Regular schedule banao, short notes likhte jao, previous papers solve karo. Pass zaroor hoge!",
          "health":"Sehat sabse badi daulat hai Boss! Regular exercise, balanced diet, poori neend — zaruri hain.",
          "education":"Shiksha sabse powerful weapon hai! Yeh career, thinking aur life improve karti hai.",
          "business":"Business mein risk aur reward dono hain! Achha idea + mehnat + patience = success!",
          "love":"Pyar ek khoobsurat ehsaas hai Boss! Yeh relationships ko mazboot banata hai.",
          "life":"Zindagi ek anmol tohfa hai Boss! Ise khushi, mehnat aur pyar se jeena chahiye.",
          "success":"Safalta ke liye clear goal set karo, mehnat karo, consistent raho, kabhi haar mat mano!",
          "music":"Music soul ki bhasha hai! Mood improve karta hai, stress kam karta hai.",
          "game":"Gaming ek popular hobby hai! PUBG, Free Fire, GTA — popular games hain.",
          "movie":"Movies ek art form hai Boss! Bollywood, Hollywood — entertainment ki duniya.",
          "food":"Khana zindagi ka important hissa hai! Biryani, dal makhani, dosa — India mein kitne delicious dishes!"}
    for k, v in kb.items():
        if k in t: return v
    deva = {"kem cho":"Hu saras chhu Boss! Tame kem cho? Hu tamari shu madad kari shakhu?",
            "kem chho":"Hu bilkul saras chhu Boss! Tame kem chho?",
            "tane kone banayu":"Mane Ritik Boss e banavio chhe! Hu JARVIS RK chhu, temno personal AI assistant.",
            "kon chhe tu":"Hu JARVIS RK chhu, Ritik Boss no personal AI assistant!",
            "narendra modi":"Narendra Modi India na 14ma Prime Minister chhe. 2014 thi PM chhe.",
            "parul":"Parul University Vadodara, Gujarat ma chhe. Engineering, medical, management courses offer kare chhe.",
            "कैसे हो":"Main bilkul theek hoon Boss! Aap kaise hain? Kya madad kar sakta hoon?",
            "नरेंद्र मोदी":"Narendra Modi India ke 14ve Prime Minister hain. 2014 se PM hain.",
            "मोदी":"Narendra Modi India ke Prime Minister hain. BJP ke neta hain.",
            "पारुल":"Parul University Vadodara, Gujarat mein hai. Engineering, medical, management courses offer karti hai.",
            "वडोदरा":"Vadodara Gujarat ka ek important sheher hai. Baroda ke naam se bhi jaana jaata hai."}
    for k, v in deva.items():
        if k in raw.lower() or k in t: return v
    return {"hi":f"Boss, samajh gaya! Kya aap aur detail mein bata sakte hain?",
            "en":f"Boss, got it! Can you give more details?",
            "gu":f"Boss, samji gayo! Thodu vahu detail aapi shako?",
            "mr":f"Boss, samjalo! Thodi jast mahiti deu shakata ka?"}.get(lang,"Boss, samajh gaya!")

def cmd(t, raw, lang):
    if any(w in t for w in ["gujarati me","gujarati mein","gujarati ma"]): return "Okay Boss! Hu havi Gujarati ma vaat karish!","set_lang_gu",""
    if any(w in t for w in ["marathi me","marathi mein","marathi madhe"]): return "Okay Boss! Aata mi Marathi madhe bolto!","set_lang_mr",""
    if any(w in t for w in ["hindi me","hindi mein","speak hindi"]): return "Okay Boss! Ab main Hindi mein bolunga!","set_lang_hi",""
    if any(w in t for w in ["english me","speak english","english mein"]): return "Sure Boss! Speaking in English now!","set_lang_en",""
    if any(w in t for w in ["shutdown","pc band karo","system band karo"]): os.system("shutdown /s /t 10"); return "Boss, system 10s mein shutdown!","none",""
    if any(w in t for w in ["restart","reboot","pc restart"]): os.system("shutdown /r /t 10"); return "Boss, system restart!","none",""
    if any(w in t for w in ["volume up","awaz badhao","awaaz badhao"]):
        try: [ctypes.windll.user32.keybd_event(0xAF,0,0,0) for _ in range(5)]
        except: pass
        return "Awaaz badha di Boss!","none",""
    if any(w in t for w in ["volume down","awaz kam","awaaz kam"]):
        try: [ctypes.windll.user32.keybd_event(0xAE,0,0,0) for _ in range(5)]
        except: pass
        return "Awaaz kam kar di Boss!","none",""
    if "mute" in t:
        try: ctypes.windll.user32.keybd_event(0xAD,0,0,0)
        except: pass
        return "Mute kar diya Boss!","none",""
    if any(w in t for w in ["battery","charge"]):
        res = subprocess.run("powershell (Get-CimInstance -ClassName Win32_Battery).EstimatedChargeRemaining",capture_output=True,text=True,shell=True).stdout.strip()
        return (f"Boss, battery {res}% hai!" if res and res.isdigit() else "Boss, battery info nahi mili."),"none",""
    if any(w in t for w in ["screenshot","screen capture"]):
        ps = ("[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms');[Reflection.Assembly]::LoadWithPartialName('System.Drawing');$s=[System.Windows.Forms.Screen]::PrimaryScreen;$b=New-Object System.Drawing.Bitmap($s.Bounds.Width,$s.Bounds.Height);$g=[System.Drawing.Graphics]::FromImage($b);$g.CopyFromScreen($s.Bounds.X,$s.Bounds.Y,0,0,$b.Size);$b.Save('screenshot.png',[System.Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$b.Dispose();")
        subprocess.run(["powershell","-Command",ps],shell=True)
        return "Screenshot le liya Boss!","none",""
    if any(w in t for w in ["time","kitne baje","samay"]):
        now = datetime.now()
        return {"hi":f"Boss, abhi {now.strftime('%I:%M %p')} baje hain!","en":f"Boss, it is {now.strftime('%I:%M %p')}!","gu":f"Boss, abhi {now.strftime('%I:%M %p')} vagya chhe!","mr":f"Boss, aata {now.strftime('%I:%M %p')} vajale!"}.get(lang,f"Abhi {now.strftime('%I:%M %p')} baje hain!"),"none",""
    if any(w in t for w in ["date","tarikh","aaj kya"]):
        now = datetime.now()
        return {"hi":f"Boss, aaj {now.strftime('%d %B %Y')} hai!","en":f"Boss, today is {now.strftime('%d %B %Y')}!","gu":f"Boss, aaj {now.strftime('%d %B %Y')} chhe!","mr":f"Boss, aaj {now.strftime('%d %B %Y')} aahe!"}.get(lang,f"Aaj {now.strftime('%d %B %Y')} hai!"),"none",""
    if any(w in t for w in ["close","band karo","band kar","kill"]):
        cm = {"chrome":"chrome.exe","notepad":"notepad.exe","paint":"mspaint.exe","vs code":"Code.exe","vscode":"Code.exe"}
        for n,e in cm.items():
            if n in t: os.system(f"taskkill /IM {e} /F"); return f"{n.title()} band kar diya Boss!","none",""
    if (("play" in t or "chalao" in t) and ("youtube" in t or "song" in t or "music" in t or "gana" in t)) or "gaana" in t:
        q = t
        for w in ["play","on youtube","youtube par","youtube","chalao","song","gana","gaana","music","par","open","kholo"]: q = q.replace(w,"")
        q = q.strip()
        if q and len(q)>1:
            url = "https://www.youtube.com/results?search_query="+urllib.parse.quote(q)
            webbrowser.open(url); return f"YouTube par '{q}' chala raha hoon Boss!","open_url",url
        webbrowser.open("https://youtube.com"); return "YouTube khol diya Boss!","open_url","https://youtube.com"
    if "google" in t and any(w in t for w in ["search","khojo","dhundo","karo","par"]):
        q = t
        for w in ["google par search karo","search on google","google mein search karo","google search","google","search","karo","par"]: q = q.replace(w,"")
        q = q.strip()
        if q and len(q)>1:
            url = "https://www.google.com/search?q="+urllib.parse.quote(q)
            webbrowser.open(url); return f"Google par '{q}' search kar raha hoon Boss!","open_url",url
    SITES = {"youtube":("https://youtube.com","YouTube khol diya Boss!"),"whatsapp":("https://web.whatsapp.com","WhatsApp khol diya Boss!"),"instagram":("https://instagram.com","Instagram khol diya Boss!"),"facebook":("https://facebook.com","Facebook khol diya Boss!"),"twitter":("https://twitter.com","Twitter khol diya Boss!"),"gmail":("https://mail.google.com","Gmail khol diya Boss!"),"google":("https://google.com","Google khol diya Boss!"),"github":("https://github.com","GitHub khol diya Boss!"),"netflix":("https://netflix.com","Netflix khol diya Boss!")}
    APPS = {"chrome":"start chrome","notepad":"notepad","calculator":"calc","paint":"mspaint","cmd":"start cmd","settings":"start ms-settings:","file explorer":"explorer","vs code":"code","vscode":"code","task manager":"taskmgr","camera":"start microsoft.windows.camera:"}
    OW = ["open","kholo","launch","start","chalao","khol","ughad"]
    if any(w in t for w in OW) or any(w in raw for w in ["ओपन","खोलो"]):
        for s,(u,m) in SITES.items():
            if s in t: webbrowser.open(u); return m,"open_url",u
        for n,c in APPS.items():
            if n in t: os.system(c); return f"{n.title()} khol diya Boss!","none",""
    for s,(u,m) in SITES.items():
        if s in t: webbrowser.open(u); return m,"open_url",u
    return None

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse((BASE/"index.html").read_text(encoding="utf-8"))

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_msg = str(data.get("message","")).strip()
        lang = str(data.get("lang","hi"))
        sid = str(data.get("session","default"))
        dl = detect_lang(user_msg)
        if dl: lang = dl
        t = user_msg.lower().strip()
        print(f"\n[USER|{lang}] {user_msg}")
        if not t: return JSONResponse({"reply":"Haan Boss, boliye!","action":"none","url":""})
        hist = get_hist(sid)
        m = re.search(r"(?:my name is|mera naam|maro naam)\s+([A-Za-z]+)", user_msg, re.I)
        if m: _names[sid] = m.group(1).title()
        if any(w in t for w in ["mera naam kya","what is my name"]):
            n = _names.get(sid)
            return JSONResponse({"reply":f"Aapka naam {n} hai Boss!" if n else "Boss, naam nahi bataya!","action":"none","url":""})
        r = cmd(t, user_msg, lang)
        if r:
            reply, action, url = r
            print(f"[CMD] {reply[:50]}")
            return JSONResponse({"reply":reply,"action":action,"url":url})
        hist.append({"role":"user","msg":user_msg})
        reply = ask_ai(user_msg, lang, hist, _names.get(sid,"")) or fallback(user_msg, lang)
        hist.append({"role":"assistant","msg":reply})
        print(f"[AI] {reply[:60]}")
        return JSONResponse({"reply":reply,"action":"none","url":""})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"reply":fallback(str(data.get("message","")),str(data.get("lang","hi"))),"action":"none","url":""})
