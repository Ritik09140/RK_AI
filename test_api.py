import os, pathlib, json, urllib.request

GEMINI_KEY = "AIzaSyDt-3-p6zrbaxYv5TwIGpxpIJ6wXea5das"
sys_p = "You are RK."
prompt = sys_p + "\n\nUser: hello\nRK:"
body_g = json.dumps({
    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.8}
}).encode()

try:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_KEY
    req = urllib.request.Request(url, data=body_g, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read().decode())
        print(d["candidates"][0]["content"]["parts"][0]["text"].strip())
except Exception as e:
    import traceback
    traceback.print_exc()
