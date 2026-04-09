
new_views = '''import os
import sys
import json
import ctypes
import urllib.parse
import subprocess
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'assistant/index.html')


@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        data = json.loads(request.body)
        user_msg = data.get('message', '').strip()
        client_lang = data.get('client_lang', 'hi')
        text_low = user_msg.lower()

        lang_triggers = {
            'gujarati me bat':  ('gu', 'Ab hu Gujarati ma vaat karish.'),
            'gujarati me baat': ('gu', 'Ab hu Gujarati ma vaat karish.'),
            'marathi me bat':   ('mr', 'Aata mi Marathi madhe bolto.'),
            'marathi me baat':  ('mr', 'Aata mi Marathi madhe bolto.'),
            'hindi me bat':     ('hi', 'Theek hai boss, ab main Hindi mein baat karunga.'),
            'hindi me baat':    ('hi', 'Theek hai boss, ab main Hindi mein baat karunga.'),
            'english me bat':   ('en', 'Alright boss, switching to English.'),
            'english me baat':  ('en', 'Alright boss, switching to English.'),
        }
        for trigger, (code, resp) in lang_triggers.items():
            if trigger in text_low:
                return JsonResponse({'reply': resp, 'action': 'set_lang_' + code, 'url': ''})

        if any(w in text_low for w in ['kisne banaya', 'who created', 'who made', 'creator']):
            replies = {
                'hi': 'Mujhe mere boss Ritik ne banaya hai. Main RK hoon.',
                'en': 'I was created by my boss Ritik. I am RK.',
                'gu': 'Mane mara boss Ritik e banavio chhe. Hu RK chhu.',
                'mr': 'Mala mazya boss Ritikne banawale aahe. Mi RK aahe.',
            }
            return JsonResponse({'reply': replies.get(client_lang, replies['hi']), 'action': 'none', 'url': ''})

        if text_low.strip() in ['tum kaun ho', 'who are you', 'hello', 'hi', 'hey']:
            replies = {
                'hi': 'Hello Boss Ritik! Main aapka personal AI RK hoon. Ritik boss ne mujhe banaya hai.',
                'en': 'Hello Boss Ritik! I am your personal AI RK, created by Ritik Boss.',
                'gu': 'Hello Boss Ritik! Hu tamaro personal AI RK chhu.',
                'mr': 'Hello Boss Ritik! Mi tumcha personal AI RK aahe.',
            }
            return JsonResponse({'reply': replies.get(client_lang, replies['hi']), 'action': 'none', 'url': ''})

        if any(w in text_low for w in ['shutdown', 'pc band karo', 'system band karo']):
            os.system('shutdown /s /t 10')
            return JsonResponse({'reply': 'Boss, system 10 seconds mein shutdown ho raha hai.', 'action': 'none', 'url': ''})

        if any(w in text_low for w in ['restart', 'pc restart', 'reboot']):
            os.system('shutdown /r /t 10')
            return JsonResponse({'reply': 'Boss, system restart ho raha hai.', 'action': 'none', 'url': ''})

        if any(w in text_low for w in ['volume up', 'awaz badhao']):
            try:
                for _ in range(5): ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            except: pass
            return JsonResponse({'reply': 'Awaaz badha di boss.', 'action': 'none', 'url': ''})

        if any(w in text_low for w in ['volume down', 'awaz kam karo']):
            try:
                for _ in range(5): ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            except: pass
            return JsonResponse({'reply': 'Awaaz kam kar di boss.', 'action': 'none', 'url': ''})

        if 'mute' in text_low:
            try: ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            except: pass
            return JsonResponse({'reply': 'Mute kar diya boss.', 'action': 'none', 'url': ''})

        if any(w in text_low for w in ['battery', 'charge']):
            res = subprocess.run('powershell (Get-CimInstance -ClassName Win32_Battery).EstimatedChargeRemaining', capture_output=True, text=True, shell=True).stdout.strip()
            if res and res.isdigit():
                return JsonResponse({'reply': 'Boss, battery abhi ' + res + '% hai.', 'action': 'none', 'url': ''})
            return JsonResponse({'reply': 'Boss, battery info nahi mili.', 'action': 'none', 'url': ''})

        if any(w in text_low for w in ['screenshot', 'screen capture']):
            ps = "[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms');[Reflection.Assembly]::LoadWithPartialName('System.Drawing');$s=[System.Windows.Forms.Screen]::PrimaryScreen;$b=New-Object System.Drawing.Bitmap($s.Bounds.Width,$s.Bounds.Height);$g=[System.Drawing.Graphics]::FromImage($b);$g.CopyFromScreen($s.Bounds.X,$s.Bounds.Y,0,0,$b.Size);$b.Save('screenshot.png',[System.Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$b.Dispose();"
            subprocess.run(['powershell', '-Command', ps], shell=True)
            return JsonResponse({'reply': 'Screenshot le liya boss.', 'action': 'none', 'url': ''})

        if any(t in text_low for t in ['open', 'kholo', 'start', 'launch']):
            apps = {
                'camera': 'start microsoft.windows.camera:',
                'calculator': 'calc', 'notepad': 'notepad', 'paint': 'mspaint',
                'cmd': 'start cmd', 'settings': 'start ms-settings:',
                'file explorer': 'explorer', 'vs code': 'code', 'vscode': 'code',
                'chrome': 'start chrome', 'whatsapp': 'start whatsapp:', 'task manager': 'taskmgr',
            }
            for app_name, sys_cmd in apps.items():
                if app_name in text_low:
                    try: os.system(sys_cmd)
                    except: pass
                    if app_name == 'whatsapp':
                        return JsonResponse({'reply': 'WhatsApp khol raha hoon boss.', 'action': 'open_url', 'url': 'https://web.whatsapp.com'})
                    return JsonResponse({'reply': app_name.title() + ' khol diya boss.', 'action': 'none', 'url': ''})

        if any(t in text_low for t in ['close', 'band karo', 'kill']):
            close_map = {'chrome': 'chrome.exe', 'notepad': 'notepad.exe', 'vs code': 'Code.exe', 'paint': 'mspaint.exe'}
            for name, exe in close_map.items():
                if name in text_low:
                    os.system('taskkill /IM ' + exe + ' /F')
                    return JsonResponse({'reply': name.title() + ' band kar diya boss.', 'action': 'none', 'url': ''})

        if 'whatsapp' in text_low:
            return JsonResponse({'reply': 'WhatsApp khol raha hoon.', 'action': 'open_url', 'url': 'https://web.whatsapp.com'})

        yt_play = ('play' in text_low and 'youtube' in text_low) or ('chalao' in text_low and 'youtube' in text_low) or ('play' in text_low and 'song' in text_low)
        if yt_play:
            query = text_low.replace('play','').replace('on youtube','').replace('youtube','').replace('chalao','').replace('song','').strip()
            if query:
                return JsonResponse({'reply': 'YouTube par ' + query + ' chala raha hoon boss.', 'action': 'open_url', 'url': 'https://www.youtube.com/results?search_query=' + urllib.parse.quote(query)})

        if 'youtube' in text_low:
            return JsonResponse({'reply': 'YouTube khol raha hoon.', 'action': 'open_url', 'url': 'https://youtube.com'})

        if 'google' in text_low:
            query = text_low.replace('search on google','').replace('google par search karo','').replace('google','').strip()
            if query:
                return JsonResponse({'reply': 'Google par ' + query + ' khoj raha hoon.', 'action': 'open_url', 'url': 'https://www.google.com/search?q=' + urllib.parse.quote(query)})
            return JsonResponse({'reply': 'Google khol raha hoon.', 'action': 'open_url', 'url': 'https://google.com'})

        if any(w in text_low for w in ['time', 'kitne baje', 'date', 'aaj ki tarikh']):
            from datetime import datetime
            now = datetime.now()
            return JsonResponse({'reply': 'Boss, abhi ' + now.strftime('%I:%M %p') + ' baje hain, aaj ' + now.strftime('%d %B %Y') + ' hai.', 'action': 'none', 'url': ''})

        lang_map_full = {'hi': 'Hindi', 'gu': 'Gujarati', 'mr': 'Marathi', 'en': 'English'}
        target_lang = lang_map_full.get(client_lang, 'Hindi')
        prompt = 'You are RK, a NEXT-GENERATION AI PERSONAL ASSISTANT created by Ritik Boss. Personality: Smart, confident, helpful, futuristic like JARVIS. CRITICAL: Respond ONLY in ' + target_lang + '. Keep it concise (2-3 sentences). User: ' + user_msg
        safe_prompt = prompt.replace(chr(39)*3, '---')
        tq = chr(39)*3
        g4f_lines = [
            'import sys,asyncio,io',
            'sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")',
            'asyncio.set_event_loop(asyncio.new_event_loop())',
            'try:',
            '    from g4f.client import Client',
            '    c=Client()',
            '    r=c.chat.completions.create(model="gpt-4o",messages=[{"role":"user","content":' + tq + safe_prompt + tq + '}])',
            '    print("AI:"+r.choices[0].message.content.strip())',
            'except Exception as e:',
            '    print("ERROR:"+str(e))',
        ]
        g4f_code = '\n'.join(g4f_lines)
        try:
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            result = subprocess.run([sys.executable, '-c', g4f_code], capture_output=True, text=True, timeout=20, env=env, encoding='utf-8')
            output = result.stdout.strip()
            if output.startswith('AI:'):
                reply = output[3:].strip()
            else:
                err = output.replace('ERROR:','').strip() or result.stderr.strip()
                reply = 'Sorry boss, AI response nahi mila. (' + err[:80] + ')'
        except subprocess.TimeoutExpired:
            reply = 'Boss, AI server slow hai. Please dobara poochiye.'
        except Exception as e:
            reply = 'System error boss. (' + str(e)[:60] + ')'

        return JsonResponse({'reply': reply, 'action': 'none', 'url': ''})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
'''

with open('assistant/views.py', 'w', encoding='utf-8') as f:
    f.write(new_views)

import ast
ast.parse(new_views)
print('OK - views.py written and syntax verified')
