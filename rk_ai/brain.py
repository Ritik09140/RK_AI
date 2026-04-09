"""RK AI Brain — Smart NLP + Memory + Personality Engine"""
import random, re
from datetime import datetime
from collections import deque

# ── Conversation Memory (per session) ────────────────────────────────────────
class Memory:
    def __init__(self):
        self.history = deque(maxlen=10)
        self.user_name = None
        self.user_info = {}

    def add(self, role: str, msg: str):
        self.history.append({"role": role, "msg": msg, "time": datetime.now()})

    def get_context(self) -> str:
        return " | ".join([f"{h['role']}: {h['msg']}" for h in list(self.history)[-5:]])

    def learn(self, msg: str):
        # Extract name
        m = re.search(r"(?:my name is|mera naam|maro naam|maza nav)\s+([A-Za-z]+)", msg, re.I)
        if m:
            self.user_name = m.group(1).title()
        # Extract city
        m2 = re.search(r"(?:i am from|main.*?se hoon|hu.*?no chhu|mi.*?ahe)\s+([A-Za-z]+)", msg, re.I)
        if m2:
            self.user_info["city"] = m2.group(1).title()

# Global memory store (session-based)
_sessions: dict[str, Memory] = {}

def get_memory(session_id: str = "default") -> Memory:
    if session_id not in _sessions:
        _sessions[session_id] = Memory()
    return _sessions[session_id]


# ── Personality Responses ─────────────────────────────────────────────────────
def pick(*options):
    return random.choice(options)

GREET = {
    "hi": [
        "Hello Boss! 😎 Main bilkul ready hoon. Aap kaise hain? Kya kar sakte hain aapke liye?",
        "Kya haal hai Boss! 🔥 Main hamesha aapki seva mein hazir hoon. Boliye!",
        "Namaste Boss! 💯 Aap aa gaye — ab kaam shuru karte hain. Kya chahiye?",
        "Hey Boss! 😄 Main theek hoon, aap batao — kya madad kar sakta hoon?",
    ],
    "en": [
        "Hey Boss! 😎 I'm all set and ready. How are you doing? What can I do for you?",
        "Hello Boss! 🔥 Always at your service. What's up?",
        "What's good Boss! 💯 Ready to roll. What do you need?",
    ],
    "gu": [
        "Hello Boss! 😎 Hu tamari seva ma taiyar chhu. Tame kem cho? Shu kari shakhu?",
        "Kem cho Boss! 🔥 Hu hamesha tamari paase chhu. Bolo!",
        "Namaste Boss! 💯 Tame aavya — hu taiyar chhu. Shu joie chhe?",
    ],
    "mr": [
        "Hello Boss! 😎 Mi tumchi seva karat aahe. Tum kase aahat? Kay karu?",
        "Kasa aahe Boss! 🔥 Mi hamesha tumchyasathe aahe. Sanga!",
        "Namaste Boss! 💯 Tum aala — mi taiyar aahe. Kay pahije?",
    ],
}

HOW_ARE_YOU = {
    "hi": [
        "Main ekdum mast hoon Boss! 😎 Aap batao, kya chal raha hai?",
        "Bilkul theek hoon Boss! 🔥 Aapki seva mein hamesha ready. Aap kaise hain?",
        "Top form mein hoon Boss! 💯 Koi kaam ho toh batao!",
    ],
    "en": [
        "I'm doing awesome Boss! 😎 What about you? How's everything going?",
        "Feeling great Boss! 🔥 Always ready to serve. How are you?",
        "Top of the world Boss! 💯 What can I do for you today?",
    ],
    "gu": [
        "Hu mast chhu Boss! 😎 Tame kevo chho? Shu chal rahu chhe?",
        "Bilkul saras chhu Boss! 🔥 Tamari seva ma hamesha ready. Tame kem cho?",
        "Top form ma chhu Boss! 💯 Koi kaam hoy to kaho!",
    ],
    "mr": [
        "Mi mast aahe Boss! 😎 Tum kase aahat? Kay challay?",
        "Bilkul chhan aahe Boss! 🔥 Tumchi seva karat hamesha ready. Tum kase aahat?",
        "Top form madhe aahe Boss! 💯 Kahi kaam asel tar sanga!",
    ],
}

DONE = {
    "hi": ["Done Boss! 🔥", "Ho gaya Boss! 💯", "Kaam ho gaya Boss! 😎", "Bilkul Boss! ✅"],
    "en": ["Done Boss! 🔥", "Got it Boss! 💯", "All done Boss! 😎", "Sure thing Boss! ✅"],
    "gu": ["Thayun Boss! 🔥", "Ho gayu Boss! 💯", "Kaam thayun Boss! 😎", "Bilkul Boss! ✅"],
    "mr": ["Zale Boss! 🔥", "Ho gale Boss! 💯", "Kaam zale Boss! 😎", "Nakki Boss! ✅"],
}


# ── Knowledge Base ────────────────────────────────────────────────────────────
KNOWLEDGE = {
    # Programming
    "python": {
        "hi": ["Python ek powerful programming language hai jo AI, web development aur automation mein use hoti hai. 🐍 Iska syntax simple hai isliye beginners ke liye best hai!", "Python — duniya ki sabse popular language! 🔥 AI, ML, web, automation — sab mein use hoti hai. Guido van Rossum ne 1991 mein banaya tha."],
        "en": ["Python is a powerful, easy-to-learn programming language used in AI, web development, and automation! 🐍", "Python — the world's most popular language! 🔥 Used in AI, ML, web, automation. Created by Guido van Rossum in 1991."],
        "gu": ["Python ek powerful programming language chhe jo AI, web development ane automation ma use thay chhe. 🐍 Eno syntax simple chhe!", "Python — duniya ni sabse popular language! 🔥 AI, ML, web, automation — badha ma use thay chhe."],
        "mr": ["Python ek powerful programming language aahe jo AI, web development ani automation madhe vaparate. 🐍 Yacha syntax simple aahe!", "Python — jagaatil sabse popular language! 🔥 AI, ML, web, automation — sarvatra vaparate."],
    },
    "java": {
        "hi": ["Java ek object-oriented programming language hai jo 'Write Once, Run Anywhere' principle follow karta hai. ☕ Android apps aur enterprise software mein widely use hota hai!", "Java — robust aur platform-independent language! ☕ James Gosling ne 1995 mein banaya. Android development ka backbone hai."],
        "en": ["Java is an object-oriented language following 'Write Once, Run Anywhere'! ☕ Widely used in Android and enterprise software.", "Java — robust and platform-independent! ☕ Created by James Gosling in 1995. The backbone of Android development."],
        "gu": ["Java ek object-oriented programming language chhe. ☕ Android apps ane enterprise software ma widely use thay chhe!", "Java — robust ane platform-independent language! ☕ James Gosling e 1995 ma banavio."],
        "mr": ["Java ek object-oriented programming language aahe. ☕ Android apps ani enterprise software madhe widely vaparate!", "Java — robust ani platform-independent! ☕ James Gosling ne 1995 madhe banawale."],
    },
    "javascript": {
        "hi": ["JavaScript web ka king hai! 👑 Websites ko interactive banata hai. Frontend mein React, backend mein Node.js — har jagah JS hai!", "JS — ek language jo browser mein directly run hoti hai. 🌐 Aaj duniya ki sabse zyada use hone wali language hai!"],
        "en": ["JavaScript is the king of the web! 👑 Makes websites interactive. React for frontend, Node.js for backend — JS is everywhere!", "JS runs directly in browsers! 🌐 The most widely used language in the world today!"],
        "gu": ["JavaScript web no king chhe! 👑 Websites ne interactive banave chhe. Frontend ma React, backend ma Node.js!", "JS browser ma directly run thay chhe. 🌐 Aaj duniya ni sabse vahu use thati language chhe!"],
        "mr": ["JavaScript web cha king aahe! 👑 Websites interactive banawato. Frontend madhe React, backend madhe Node.js!", "JS browser madhe directly run hoto. 🌐 Aaj jagaatil sabse jast vaparate janarya language aahe!"],
    },
    "ai": {
        "hi": ["AI yaani Artificial Intelligence — machines ko insaan ki tarah sochne ki ability! 🤖 Machine Learning, Deep Learning, NLP — sab AI ke parts hain. Future AI ka hai Boss!", "Artificial Intelligence ek revolutionary technology hai. 🚀 Healthcare, finance, robotics, education — har field mein AI aa raha hai!"],
        "en": ["AI — Artificial Intelligence gives machines the ability to think like humans! 🤖 ML, Deep Learning, NLP — all parts of AI. The future belongs to AI Boss!", "AI is a revolutionary technology! 🚀 Healthcare, finance, robotics, education — AI is entering every field!"],
        "gu": ["AI yaane Artificial Intelligence — machines ne insaan jevi sochvani ability! 🤖 ML, Deep Learning, NLP — badha AI na parts chhe. Future AI no chhe Boss!", "AI ek revolutionary technology chhe. 🚀 Healthcare, finance, robotics — badha fields ma AI aavi rahu chhe!"],
        "mr": ["AI mhanje Artificial Intelligence — machines la manasasarkha vicharnyachi kshamata! 🤖 ML, Deep Learning, NLP — he sab AI che bhag aahet. Bhavishya AI che aahe Boss!", "AI ek revolutionary technology aahe. 🚀 Healthcare, finance, robotics — pratyek field madhe AI yeto aahe!"],
    },
    "machine learning": {
        "hi": ["Machine Learning AI ka dil hai! 💡 Computers data se khud seekhte hain. Supervised, Unsupervised aur Reinforcement Learning — teen types hain. Netflix recommendations, spam filters — sab ML hai!", "ML mein algorithms data patterns dhundhte hain. 🧠 Jitna zyada data, utna smart model!"],
        "en": ["Machine Learning is the heart of AI! 💡 Computers learn from data automatically. Netflix recommendations, spam filters — all ML!", "ML algorithms find patterns in data. 🧠 More data = smarter model!"],
        "gu": ["Machine Learning AI nu dil chhe! 💡 Computers data thi khud shikhay chhe. Netflix recommendations, spam filters — badhu ML chhe!", "ML ma algorithms data patterns shodhay chhe. 🧠 Jitna vahu data, utno smart model!"],
        "mr": ["Machine Learning AI che hriday aahe! 💡 Computers data pasun khud shiktat. Netflix recommendations, spam filters — he sab ML aahe!", "ML madhe algorithms data patterns shodhtat. 🧠 Jitka jast data, titka smart model!"],
    },
    "india": {
        "hi": ["India — Bharat Mata ki Jai! 🇮🇳 1.4 billion logon ka desh, duniya ka sabse bada democracy. Ancient civilization, diverse culture, aur ab technology superpower ban raha hai!", "India ek mahan desh hai. 🇮🇳 Yahan 22 official languages, 28 states hain. Space, IT, medicine — har field mein India aage badh raha hai!"],
        "en": ["India — Jai Hind! 🇮🇳 1.4 billion people, world's largest democracy. Ancient civilization, diverse culture, and now becoming a tech superpower!", "India is a great nation! 🇮🇳 22 official languages, 28 states. Space, IT, medicine — India is advancing in every field!"],
        "gu": ["India — Bharat Mata ki Jai! 🇮🇳 1.4 billion logon no desh, duniya no sabse moto democracy. Ancient civilization ane diverse culture!", "India ek mahan desh chhe. 🇮🇳 22 official languages, 28 states. Space, IT, medicine — badha fields ma India aage vadhi rahu chhe!"],
        "mr": ["India — Bharat Mata ki Jai! 🇮🇳 1.4 billion loganche desh, jagaatil sabse motha democracy. Prachin sanskriti ani vividh sanskriti!", "India ek mahan desh aahe. 🇮🇳 22 official languages, 28 states. Space, IT, medicine — pratyek field madhe India pudhe jato aahe!"],
    },
    "cricket": {
        "hi": ["Cricket India ka dharam hai Boss! 🏏 Virat Kohli, Rohit Sharma, MS Dhoni — legends! IPL duniya ki sabse popular T20 league hai. India ne 2 World Cups jeete hain!", "Cricket mein 11-11 khiladiyon ki 2 teams hoti hain. 🏏 Test, ODI, T20 — teen formats hain. India ka home ground Wankhede aur Eden Gardens famous hain!"],
        "en": ["Cricket is India's religion Boss! 🏏 Virat Kohli, Rohit Sharma, MS Dhoni — legends! IPL is the world's most popular T20 league!", "Cricket has 2 teams of 11 players each. 🏏 Test, ODI, T20 — three formats. India has won 2 World Cups!"],
        "gu": ["Cricket India no dharm chhe Boss! 🏏 Virat Kohli, Rohit Sharma, MS Dhoni — legends! IPL duniya ni sabse popular T20 league chhe!", "Cricket ma 11-11 khiladiyon ni 2 teams hoy chhe. 🏏 Test, ODI, T20 — tran formats chhe."],
        "mr": ["Cricket India cha dharm aahe Boss! 🏏 Virat Kohli, Rohit Sharma, MS Dhoni — legends! IPL jagaatil sabse popular T20 league aahe!", "Cricket madhe 11-11 khiladiyanchi 2 teams astat. 🏏 Test, ODI, T20 — teen formats aahet."],
    },
    "health": {
        "hi": ["Sehat hi sabse badi daulat hai Boss! 💪 Regular exercise, balanced diet, poori neend — yeh teen cheezein aapko healthy rakhti hain. Roz 30 min walk karo, paani zyada piyo!", "Health tips: 🥗 Subah jaldi utho, exercise karo, junk food kam khao, stress manage karo. Ek healthy body mein hi healthy mind rehta hai!"],
        "en": ["Health is the greatest wealth Boss! 💪 Regular exercise, balanced diet, proper sleep — these three keep you healthy. Walk 30 min daily, drink more water!", "Health tips: 🥗 Wake up early, exercise, eat less junk food, manage stress. A healthy body houses a healthy mind!"],
        "gu": ["Sehat j sabse moti daulat chhe Boss! 💪 Regular exercise, balanced diet, puri ughad — aa tran cheejo tamne healthy rakhe chhe!", "Health tips: 🥗 Savare jaldi utho, exercise karo, junk food occhu khao, stress manage karo."],
        "mr": ["Aarogya hich sabse motha sampatti aahe Boss! 💪 Regular exercise, balanced diet, puri jhop — ya teen goshti tumhala healthy thevtat!", "Health tips: 🥗 Sakali lavkar utha, exercise kara, junk food kami khaa, stress manage kara."],
    },
}

def get_knowledge(topic: str, lang: str) -> str | None:
    for key, data in KNOWLEDGE.items():
        if key in topic:
            responses = data.get(lang, data.get("hi", []))
            if responses:
                return random.choice(responses)
    return None


# ── Intent Detection ──────────────────────────────────────────────────────────
INTENTS = {
    "open_youtube": ["youtube chalao","play youtube","yt kholo","youtube open","open yt","youtube start","youtube chalu","youtube dekho","youtube par jao","open youtube","kholo youtube","youtube khol"],
    "open_chrome":  ["chrome kholo","open chrome","chrome start","chrome chalu","google chrome open","chrome launch"],
    "open_whatsapp":["whatsapp kholo","open whatsapp","whatsapp start","whatsapp chalu","wp kholo"],
    "open_google":  ["google kholo","open google","google start","google chalu","google open"],
    "open_notepad": ["notepad kholo","open notepad","notepad start","notepad chalu"],
    "play_music":   ["music chalao","gana chalao","song play karo","music play","gaana bajao","song bajao","music bajao"],
    "shutdown":     ["pc band karo","system band karo","shutdown karo","computer band","pc off karo","system off"],
    "restart":      ["restart karo","pc restart","reboot karo","system restart"],
    "volume_up":    ["awaz badhao","volume up","sound badhao","awaaz badhao","volume badha do"],
    "volume_down":  ["awaz kam karo","volume down","sound kam karo","awaaz kam","volume kam karo"],
    "screenshot":   ["screenshot lo","screen capture","screenshot le","screen shot"],
    "time":         ["time batao","kitne baje","samay batao","time kya hai","abhi kitne baje"],
    "date":         ["date batao","aaj kya date","tarikh batao","aaj kaun si date"],
    "greeting":     ["hello","hi","hey","namaste","namaskar","kem cho","kaise ho","kese ho","how are you","majama","kya haal","sup","wassup","hola"],
    "how_are_you":  ["kaise ho","kese ho","how are you","kaisa hai","kya haal hai","kem cho","majama","maza ma","kasa aahes"],
    "who_are_you":  ["tum kaun ho","who are you","rk kaun ho","aap kaun ho","tu kaun","kon chhe tu","tu kon aahe"],
    "who_made_you": ["kisne banaya","who made you","who created","creator","tumhe kisne","kaun banaya","kone banavio","konhi banawale"],
    "what_can_do":  ["kya kar sakte ho","what can you do","tumhari kya","features kya","kya kya kar sakte","help me","madad karo","capabilities"],
    "joke":         ["joke sunao","joke batao","funny kuch bolo","hasao mujhe","ek joke","jokes sunao"],
    "story":        ["kahani sunao","story sunao","ek kahani","kissa sunao","story batao"],
    "exam":         ["exam tips","pariksha tips","study tips","padhai kaise kare","exam ki taiyari","result kaise achha"],
    "weather":      ["mausam kaisa","weather kya hai","barish hogi","garmi hai","sardi hai","aaj ka mausam"],
    "news":         ["news batao","khabar sunao","aaj ki news","latest news","samachar"],
}

def detect_intent(text: str) -> str | None:
    t = text.lower()
    for intent, patterns in INTENTS.items():
        for p in patterns:
            if p in t:
                return intent
    return None
