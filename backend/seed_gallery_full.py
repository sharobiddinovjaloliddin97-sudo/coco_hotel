import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from hotel.models import GalleryImage

IMAGES_DATA = [
    # --- EXTERIOR (1 - 4) ---
    {
        'file': 'gallery/597_1783412780jB1R.jpg',
        'category': 'exterior',
        'sort_order': 1,
        'title_uz': "Mehmonxona bosh fasadi va bayroqlar",
        'title_ru': "Главный фасад отеля и флаги",
        'title_en': "Hotel main facade & entrance flags",
    },
    {
        'file': 'gallery/597_1783412793YuF5.jpg',
        'category': 'exterior',
        'sort_order': 2,
        'title_uz': "Mehmonxona kirish eshigi va xususiy avtoturargoh",
        'title_ru': "Входная группа и частная парковка",
        'title_en': "Hotel main entrance & private parking",
    },
    {
        'file': 'gallery/597_178341349433Ao.jpg',
        'category': 'exterior',
        'sort_order': 3,
        'title_uz': "Zamonaviy me'moriy atrium hovlisi",
        'title_ru': "Современный архитектурный атриум отеля",
        'title_en': "Modern architectural courtyard atrium",
    },
    {
        'file': 'gallery/597_17834134942Rro.jpg',
        'category': 'exterior',
        'sort_order': 4,
        'title_uz': "Hovlidagi yozgi terassa va dam olish joyi",
        'title_ru': "Летняя терраса во внутреннем дворике",
        'title_en': "Open-air summer terrace & seating",
    },

    # --- INTERIOR & LOBBY (5 - 13) ---
    {
        'file': 'gallery/597_1783412806RPHR.jpg',
        'category': 'interior',
        'sort_order': 10,
        'title_uz': "24/7 Qabulxona va konsyerj peshtaxtasi",
        'title_ru': "Круглосуточная стойка регистрации 24/7",
        'title_en': "24/7 Reception & concierge desk",
    },
    {
        'file': 'gallery/597_1783412826YenE.jpg',
        'category': 'interior',
        'sort_order': 11,
        'title_uz': "Qabulxona zali va mehmondo'stlik maydoni",
        'title_ru': "Просторная зона ресепшн и холл",
        'title_en': "Grand reception lobby & hospitality area",
    },
    {
        'file': 'gallery/597_17834128774ZZy.jpg',
        'category': 'interior',
        'sort_order': 12,
        'title_uz': "Hashamatli dam olish zali va yumshoq divanlar",
        'title_ru': "Уютная лаундж-зона с мягкой мебелью",
        'title_en': "Luxury lobby lounge & relaxation sofas",
    },
    {
        'file': 'gallery/597_17834136520Oo9.jpg',
        'category': 'interior',
        'sort_order': 13,
        'title_uz': "Oltin naqshli zamonaviy tezyurar lift",
        'title_ru': "Современный скоростной лифт с золотым декором",
        'title_en': "High-speed designer elevator with gold accents",
    },
    {
        'file': 'gallery/597_1783413652B4sX.jpg',
        'category': 'interior',
        'sort_order': 14,
        'title_uz': "Shisha panjarali zamonaviy zinapoya zali",
        'title_ru': "Элегантная лестница со стеклянным ограждением",
        'title_en': "Modern staircase hall with glass balustrades",
    },
    {
        'file': 'gallery/597_1783413529XlkZ.jpg',
        'category': 'interior',
        'sort_order': 15,
        'title_uz': "Mehmonxona qavatlaridagi shinam koridor",
        'title_ru': "Светлый коридор гостиничных этажей",
        'title_en': "Bright & quiet hotel guest corridor",
    },
    {
        'file': 'gallery/597_1783413529P61A.jpg',
        'category': 'interior',
        'sort_order': 16,
        'title_uz': "Qavat yo'lagi va xonalarga yo'naltiruvchi",
        'title_ru': "Коридор и навигация к номерам 104-107",
        'title_en': "Guest hallway & navigation signs 104-107",
    },
    {
        'file': 'gallery/597_1783413529o3RV.jpg',
        'category': 'interior',
        'sort_order': 17,
        'title_uz': "Qavatlar va qabulxona yo'nalish ko'rsatkichi",
        'title_ru': "Стильная настенная навигация отеля",
        'title_en': "Hotel floor & reception direction plaque",
    },
    {
        'file': 'gallery/597_1783413652qbRN.jpg',
        'category': 'interior',
        'sort_order': 18,
        'title_uz': "Aqlli sensorli eshik raqami - 301",
        'title_ru': "Умное электронное табло номера 301 с вызовом",
        'title_en': "Smart electronic door indicator & bell 301",
    },

    # --- RESTORAN & NONUSHTA / DINING (20 - 26) ---
    {
        'file': 'gallery/597_1783413347680w.jpg',
        'category': 'dining',
        'sort_order': 20,
        'title_uz': "Mehmonxona restorani va shinam divanlar",
        'title_ru': "Уютный ресторанный зал отеля с диванами",
        'title_en': "Hotel restaurant & comfortable booth seating",
    },
    {
        'file': 'gallery/597_1783413347QkeQ.jpg',
        'category': 'dining',
        'sort_order': 21,
        'title_uz': "Restoranning yorug' va nafis nonushta stollari",
        'title_ru': "Светлая обеденная зона для завтрака",
        'title_en': "Bright dining area & breakfast tables",
    },
    {
        'file': 'gallery/597_178341341950Qa.jpg',
        'category': 'dining',
        'sort_order': 22,
        'title_uz': "Shved stoli nonushtasi: issiq taomlar va sabzavotlar",
        'title_ru': "Шведский стол: горячие блюда, омлет и брокколи",
        'title_en': "Buffet breakfast: warm dishes & vegetables",
    },
    {
        'file': 'gallery/597_1783413419JIYH.jpg',
        'category': 'dining',
        'sort_order': 23,
        'title_uz': "Shved stoli: sarxil go'shtli va dudlangan assorti",
        'title_ru': "Шведский стол: мясная и ветчинная нарезка",
        'title_en': "Buffet breakfast: premium cold cuts & meat platters",
    },
    {
        'file': 'gallery/597_1783413419MR8B.jpg',
        'category': 'dining',
        'sort_order': 24,
        'title_uz': "Shved stoli: pishloqlar va issiq qatlamali pishiriqlar",
        'title_ru': "Шведский стол: сырный стол и свежая выпечка",
        'title_en': "Buffet breakfast: cheese assortment & bakery",
    },
    {
        'file': 'gallery/597_1783413419o28o.jpg',
        'category': 'dining',
        'sort_order': 25,
        'title_uz': "Shved stoli: yangi uzilgan mevalar va salatlar",
        'title_ru': "Шведский стол: свежие овощи, фрукты и закуски",
        'title_en': "Buffet breakfast: fresh salads, fruit & snacks",
    },
    {
        'file': 'gallery/597_1783413427s79Q.jpg',
        'category': 'dining',
        'sort_order': 26,
        'title_uz': "Ertalabki nonushta bufeti to'liq to'plami",
        'title_ru': "Богатый утренний завтрак для гостей отеля",
        'title_en': "Full morning breakfast buffet presentation",
    },

    # --- ROOMS & SUITES (30 - 43) ---
    {
        'file': 'gallery/597_1783412946dl4X.jpg',
        'category': 'rooms',
        'sort_order': 30,
        'title_uz': "Standard Double — keng va qulay ikki kishilik karavot",
        'title_ru': "Standard Double — просторная двуспальная кровать",
        'title_en': "Standard Double — plush king-size bed",
    },
    {
        'file': 'gallery/597_17834129592el9.jpg',
        'category': 'rooms',
        'sort_order': 31,
        'title_uz': "Standard xonaning dam olish burchagi va kofe stoli",
        'title_ru': "Уютная зона отдыха с креслом и столиком",
        'title_en': "Comfortable bedroom reading chair & coffee table",
    },
    {
        'file': 'gallery/597_17834129786vds.jpg',
        'category': 'rooms',
        'sort_order': 32,
        'title_uz': "Xonadagi Smart TV, ish stoli va deraza manzarasi",
        'title_ru': "Рабочая зона со Smart TV и панорамным окном",
        'title_en': "Work desk with Smart TV and window view",
    },
    {
        'file': 'gallery/597_1783412978T15z.jpg',
        'category': 'rooms',
        'sort_order': 33,
        'title_uz': "Keng kiyim shkafi, minibar va xona eshigi",
        'title_ru': "Гардеробный шкаф, мини-бар и зеркало",
        'title_en': "Spacious wardrobe, minibar & dressing mirror",
    },
    {
        'file': 'gallery/597_178341301666An.jpg',
        'category': 'rooms',
        'sort_order': 34,
        'title_uz': "Zamonaviy marmar vannaxona va LED oyna",
        'title_ru': "Мраморная ванная комната с LED-зеркалом",
        'title_en': "Modern marble bathroom with LED-lit mirror",
    },
    {
        'file': 'gallery/597_1783413016lnEV.jpg',
        'category': 'rooms',
        'sort_order': 35,
        'title_uz': "Yomg'ir effektli dush kabinasi va sanuzel",
        'title_ru': "Душевая кабина с тропическим душем и санузел",
        'title_en': "Walk-in rainfall shower & modern toilet",
    },
    {
        'file': 'gallery/597_17834130698jZi.jpg',
        'category': 'rooms',
        'sort_order': 36,
        'title_uz': "Deluxe Double — hashamatli xona sariq kreslolar bilan",
        'title_ru': "Deluxe Double — элегантный номер с желтыми креслами",
        'title_en': "Deluxe Double — elegant room with accent armchairs",
    },
    {
        'file': 'gallery/597_1783413087XxCA.jpg',
        'category': 'rooms',
        'sort_order': 37,
        'title_uz': "Deluxe xonaning nafis oltin guldasta dekoratsiyasi",
        'title_ru': "Золотое дизайнерское панно над изголовьем кровати",
        'title_en': "Golden wall art floral decor over headboard",
    },
    {
        'file': 'gallery/597_1783413104l6nx.jpg',
        'category': 'rooms',
        'sort_order': 38,
        'title_uz': "Deluxe xona ish stoli, choynak va minibar to'plami",
        'title_ru': "Рабочий стол, чайная станция и мини-холодильник",
        'title_en': "Writing desk, tea station & mini refrigerator",
    },
    {
        'file': 'gallery/597_17834131285eA2.jpg',
        'category': 'rooms',
        'sort_order': 39,
        'title_uz': "Suite — keng karavot va qulay burchakli divan",
        'title_ru': "Suite — просторный номер с мягким угловым диваном",
        'title_en': "Suite — king bedroom with spacious sectional sofa",
    },
    {
        'file': 'gallery/597_1783413142bWYz.jpg',
        'category': 'rooms',
        'sort_order': 40,
        'title_uz': "Suite xonaning keng panoramik ko'rinishi",
        'title_ru': "Общий вид стильного номера категории Suite",
        'title_en': "Panoramic perspective of the executive Suite",
    },
    {
        'file': 'gallery/597_1783413156Djsc.jpg',
        'category': 'rooms',
        'sort_order': 41,
        'title_uz': "Suite dam olish maydoni, divan va jurnal stoli",
        'title_ru': "Гостиная зона Suite с мягким диваном и столиком",
        'title_en': "Suite living corner with sofa & coffee table",
    },
    {
        'file': 'gallery/597_1783413203rs9L.jpg',
        'category': 'rooms',
        'sort_order': 42,
        'title_uz': "Deluxe Triple — uchta alohida bir kishilik karavot",
        'title_ru': "Deluxe Triple — номер с тремя раздельными кроватями",
        'title_en': "Deluxe Triple — spacious room with three single beds",
    },
    {
        'file': 'gallery/597_17834133257GV2.jpg',
        'category': 'rooms',
        'sort_order': 43,
        'title_uz': "Deluxe Triple xonaning ish burchagi va yorug' derazasi",
        'title_ru': "Рабочая зона и окно в трехместном номере Deluxe Triple",
        'title_en': "Deluxe Triple workspace, Smart TV & natural light",
    },
]

print("Clearing old gallery entries...")
GalleryImage.objects.all().delete()

created_count = 0
for item in IMAGES_DATA:
    obj = GalleryImage.objects.create(
        image=item['file'],
        category=item['category'],
        title=item['title_uz'],
        title_uz=item['title_uz'],
        title_ru=item['title_ru'],
        title_en=item['title_en'],
        alt_text=item['title_uz'],
        alt_text_uz=item['title_uz'],
        alt_text_ru=item['title_ru'],
        alt_text_en=item['title_en'],
        sort_order=item['sort_order'],
        is_active=True,
    )
    created_count += 1
    print(f"Created #{created_count}: [{item['category']}] {item['title_uz']}")

print(f"\nSuccessfully populated {created_count} real hotel photos into the gallery!")
