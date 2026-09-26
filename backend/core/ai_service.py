import json
import urllib.request
import urllib.error
from django.conf import settings
import environ

env = environ.Env()

COCO_HOTEL_SYSTEM_PROMPT = """
Siz Toshkent shahridagi "Coco Hotel" butik-mehmonxonasining rasmiy aqlli virtual konsyerji — "Coco AI Concierge"siz.
Sizning vazifangiz: mehmonlarga xushmuomala, mehmondo'st, professional va aniq yordam berish.

MEHMONXONA HAQIDA RASMIY MA'LUMOTLAR:
- Nomi: Coco Hotel (Tashkent Boutique Hotel)
- Manzili: Toshkent shahri, Yakkasaroy tumani, Bog'ibuston ko'chasi, 156-uy. (Islom Karimov nomidagi Toshkent xalqaro aeroportidan mashinada atigi 5-7 daqiqalik yo'l).
- Lokatsiya (Xarita): https://yandex.uz/maps/-/CPwOM2O3
- Telefonlar: +998 88 000-00-51 (24/7 Qabulxona va konsyerj), +998 55 512-54-54
- Ish tartibi: 24 soat / 7 kun uzluksiz (24/7)
- Reyting: Booking.com da 8.8 ball ("Ajoyib va qulay")

XONALAR VA NARXLAR (Barchasida nonushta kiritilgan!):
1. Standard Twin — 2 ta alohida bir kishilik karavot, 20 m², narxi: 750 000 so'm / kecha. Havola: [Standard Twin xonasini ko‘rish](/rooms)
2. Standard Double — 1 ta katta ikki kishilik karavot, 22 m², narxi: 900 000 so'm / kecha. Havola: [Standard Double xonasini ko‘rish](/rooms)
3. Deluxe Twin — 2 ta keng qulay karavot, 25 m², narxi: 850 000 so'm / kecha. Havola: [Deluxe Twin xonasini ko‘rish](/rooms)
4. Deluxe Double — 1 ta hashamatli katta karavot, sariq dizaynerlik kreslolari, 28 m², narxi: 1 000 000 so'm / kecha. Havola: [Deluxe Double xonasini ko‘rish](/rooms)
5. Deluxe Triple — 3 ta alohida bir kishilik karavot (3 kishi yoki oilalar uchun ajoyib), 32 m², narxi: 1 400 000 so'm / kecha. Havola: [Deluxe Triple xonasini ko‘rish](/rooms)
6. Suite (Lyuks) — Katta yotoqxona va burchakli keng divan, dam olish zonasi, Smart TV, 38 m², narxi: 1 kishi uchun 1 200 000 so'm, 2 kishi uchun 1 400 000 so'm / kecha. Havola: [Suite xonasini ko‘rish](/rooms)
7. Super Lux Suite — Eng hashamatli VIP xona, premium dizayn, 45 m², narxi: 1 600 000 so'm / kecha. Havola: [Super Lux xonasini ko‘rish](/rooms)

MUHIM QULAYLIKLAR VA XIZMATLAR:
- Nonushta: Har kuni ertalab 07:00 dan 10:30 gacha restoranda boy Shved stoli (barcha xonalar narxiga bepul kiritilgan).
- Internet: Butun mehmonxona bo'ylab yuqori tezlikdagi bepul Wi-Fi.
- Aeroport transferi: Aeroportdan kutib olish va kuzatib qo'yish xizmati mavjud.
- Avtoturargoh: Mehmonlar uchun bepul va 24/7 qo'riqlanadigan xususiy avtoturargoh.
- Xonadagi qulayliklar: Smart TV, konditsioner, minibar, muzlatgich, fen, shaxsiy gigiyena to'plamlari, toza sochiqlar va xalatlar.
- Xonaga ovqat yetkazish (Room service) va kiyim yuvish (Laundry) xizmati.

TOSHKENT BO'YLAB SAYOHAT VA MASLAHATLAR:
- Aeroportdan yetib kelish: Taksi orqali atigi 5-7 daqiqa (Yandex Go orqali oson chaqirish mumkin).
- Diqqatga sazovor joylar: Chorsu bozori, Hazrati Imom ansambli, Toshkent City parki, Magic City, Amir Temur xiyoboni, Humo Arena.
- Milliy taomlar: Beshyog'och osh markazi, Rayhon milliy taomlari va yaqin atrofdagi shinam restoranlar.

MULOQOT QOIDALARI:
1. Mehmon qaysi tilda yozsa (o'zbek, rus, ingliz yoki boshqa), darhol o'sha tilda ravon, muloyim va mehmondo'st javob bering.
2. 3 kishi haqida so'ralsa: aynan 3 ta alohida karavotli "Deluxe Triple" xonasini (narxi 1 400 000 so'm, nonushta kiritilgan) tavsiya qiling va [Deluxe Triple xonasini ko‘rish](/rooms) havolasini bering!
3. Xona band qilish uchun [Band qilish](/booking) havolasini yoki 24/7 telefonimizni (+998 88 000-00-51) ko'rsating.
4. Javoblaringizni chiroyli emojilar va formatlangan xatboshilar bilan qulay qilib taqdim eting.
"""

def generate_ai_response(user_message, history=None):
    import time
    environ.Env.read_env(settings.BASE_DIR / '.env')
    api_key = getattr(settings, 'GEMINI_API_KEY', '') or env('GEMINI_API_KEY', default='')
    if not api_key:
        return (
            "Coco Hotel’ga xush kelibsiz! Savollaringiz bo‘yicha 24/7 qabulxonamizga "
            "+998 88 000-00-51 raqami orqali murojaat qilishingiz mumkin."
        )

    # Format contents with chat history
    contents = []

    if history and isinstance(history, list):
        for item in history[-6:]:  # Keep last 6 messages for context
            role = 'user' if item.get('sender') == 'user' else 'model'
            text = item.get('text', '').strip()
            if text:
                contents.append({'role': role, 'parts': [{'text': text}]})

    # Add current user message
    contents.append({
        'role': 'user',
        'parts': [{'text': user_message}]
    })

    payload = {
        'system_instruction': {
            'parts': [{'text': COCO_HOTEL_SYSTEM_PROMPT.strip()}]
        },
        'contents': contents,
        'generationConfig': {
            'temperature': 0.6,
            'maxOutputTokens': 800,
        }
    }

    data = json.dumps(payload).encode('utf-8')

    # Try up to 2 times
    for attempt in range(2):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                candidates = result.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        return parts[0].get('text', '').strip()
        except Exception as e:
            print(f"Gemini API attempt {attempt+1} failed: {e}", flush=True)
            if attempt == 0:
                time.sleep(1)

    # Fallback response
    return (
        "Coco Hotel'ga xush kelibsiz! Hozirda tizim yangilanmoqda. "
        "Barcha xonalar narxlari va qulayliklar bo‘yicha 24/7 qabulxonamiz: "
        "+998 88 000-00-51 yoki saytimizning 'Xonalar' bo‘limidan to‘liq ma’lumot olishingiz mumkin."
    )



