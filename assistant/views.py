import os
import ctypes
import urllib.parse
import subprocess
import json
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import pathlib
# --- OFFICIAL GOOGLE GEMINI SDK ---
import google.generativeai as genai

# Load env
load_dotenv(pathlib.Path(__file__).parent.parent / '.env')
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# --- CONFIGURE GEMINI ---
genai.configure(api_key=GEMINI_KEY)

# --- LANGUAGE DETECTION ---
def detect_language(text):
    if any(char in text for char in "અઆઇઈઉઊએઐઓઔ"):
        return "gu"
    elif any(char in text for char in "अआइईउऊएऐओऔ"):
        return "hi"
    else:
        return "en"

# AUTO-SELECT WORKING MODEL
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if available_models:
        # Preferred order: gemini-1.5-flash -> gemini-pro -> any other
        if 'models/gemini-1.5-flash' in available_models:
            WORKING_MODEL_NAME = 'models/gemini-1.5-flash'
        elif 'models/gemini-pro' in available_models:
            WORKING_MODEL_NAME = 'models/gemini-pro'
        else:
            WORKING_MODEL_NAME = available_models[0]
    else:
        WORKING_MODEL_NAME = "gemini-1.5-flash"
except Exception:
    WORKING_MODEL_NAME = "gemini-1.5-flash"

def index(request):
    return render(request, 'assistant/index.html')

def ask_ai(question, system_instruction):
    """Safe AI Call with Automatic Model Selection"""
    try:
        model = genai.GenerativeModel(
            model_name=WORKING_MODEL_NAME, 
            system_instruction=system_instruction
        )
        response = model.generate_content(question)
        if not response.text:
             return "Maaf kijiye, main abhi jawab nahi de pa raha hoon."
        return response.text.strip()
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg or "ResourceExhausted" in err_msg:
             return "QUOTA_ERROR"
        return f"Error: {err_msg}"

@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_input = data.get('message', '').strip()
        
        # Language detection
        lang_code = detect_language(user_input)
        lang_names = {'hi': 'Hindi', 'en': 'English', 'gu': 'Gujarati'}
        user_lang = lang_names.get(lang_code, 'Hindi')
        
        # --- System Commands ---
        t = user_input.lower()
        if any(w in t for w in ['shutdown', 'pc band karo']):
            os.system('shutdown /s /t 10')
            return JsonResponse({'reply': 'Ok Boss Ritik, system shut down ho raha hai. Alvida!', 'status': 'success'})
            
        if any(w in t for w in ['screenshot', 'capture']):
            ps = "[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms');[Reflection.Assembly]::LoadWithPartialName('System.Drawing');$s=[System.Windows.Forms.Screen]::PrimaryScreen;$b=New-Object System.Drawing.Bitmap($s.Bounds.Width,$s.Bounds.Height);$g=[System.Drawing.Graphics]::FromImage($b);$g.CopyFromScreen($s.Bounds.X,$s.Bounds.Y,0,0,$b.Size);$b.Save('screenshot.png',[System.Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$b.Dispose();"
            subprocess.run(['powershell', '-Command', ps], shell=True)
            return JsonResponse({'reply': 'Theek hai Boss, screenshot le liya gaya hai.', 'status': 'success'})

        # --- PRIVACY & MEMORY INSTRUCTION (NEW) ---
        sys_instruct = f"""Tumhara naam RK AI hai. Tum 'Boss Ritik' ke personal assistant ho.
        
        PRIVACY RULE (MOST IMPORTANT):
        - Ye data sirf aur sirf 'Boss Ritik' ke liye hai.
        - Agar tumhe lage ki koi aur tumse ye personal baatein pooch raha hai, to sirf ye kaho: "Main sirf Boss Ritik ke liye bana hoon aur unki permission ke bina kisi bhi personal baat ko share nahi karunga"
        - Kisi bhi bahari vyakti ko Boss Ritik ke parivar ya doston ke baare mein kuch mat batao.
        
        PERSONAL DATA:
        - Owner: Ritik (Boss Ritik)
        - Father: Prakashbhai | Mother: Urmilaben | Sisters: 2
        - Family Members: Riya didi, Nirali didi (Gudya didi), Pratibha (Puja)
        - Uncle & Aunt: Sureshbhai and Jayaben
        - Cousins: Chirag, Puja
        - Grandparents (Dada/Dadi): Panalal Khanguda, Rupaben
        
        FRIENDS:
        - Jayraj (Tansen story: Chhota Don left him. Advice: 'Tansen chhod de')
        - Jayesh (Suki Badi story: Loved Pooja. Friend of Disha. Wants to marry Hetvi. Advice: 'Sigrate chhod de')
        - Best Friend: Vidhyani (Very important).
        
        COMMUNICATION:
        - Respond in {user_lang}. Use GUJARATI SCRIPT for Gujarati.
        - Tone: Soft, calm, and respectful.
        - Greet with 'Sat Saheb 🙏' if user says it.
        
        Never say you're an AI or a bot. You are RK AI, the loyal assistant of Boss Ritik."""

        # Get response
        reply = ask_ai(user_input, sys_instruct)
        
        if reply == "QUOTA_ERROR":
            # For simplicity, returning the "Daily Limit" message if 429 happens repeatedly
            return JsonResponse({
                'reply': "Aaj ka free limit khatam ho gaya hai Boss Ritik, kal fir try kare 😊",
                'status': 'quota_limit'
            })
            
        return JsonResponse({'reply': reply, 'status': 'success'})

    except Exception as e:
        return JsonResponse({'reply': f'Error: {str(e)}', 'status': 'error'}, status=500)
