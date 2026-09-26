import io
import os
from datetime import date, time, timedelta
from decimal import Decimal
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont

from hotel.models import HotelInformation, Service, GalleryImage, Promotion
from rooms.models import Room, RoomImage, Amenity


def create_luxury_placeholder_image(title, subtitle="COCO HOTEL", width=1200, height=800, bg_color=(20, 18, 16), accent_color=(197, 168, 128)):
    """
    Generate an elegant, high-resolution placeholder image with a dark luxury aesthetic.
    Uses charcoal/stone background, gold geometric border, and clean typography.
    """
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Outer decorative gold border
    margin = 40
    draw.rectangle(
        [(margin, margin), (width - margin, height - margin)],
        outline=accent_color,
        width=2
    )

    # Inner subtle border
    inner_margin = 48
    inner_color = (accent_color[0] // 2, accent_color[1] // 2, accent_color[2] // 2)
    draw.rectangle(
        [(inner_margin, inner_margin), (width - inner_margin, height - inner_margin)],
        outline=inner_color,
        width=1
    )

    # Corner accents
    corner_size = 20
    for cx, cy, dx, dy in [
        (margin, margin, 1, 1),
        (width - margin, margin, -1, 1),
        (margin, height - margin, 1, -1),
        (width - margin, height - margin, -1, -1)
    ]:
        draw.line([(cx, cy), (cx + dx * corner_size, cy)], fill=accent_color, width=3)
        draw.line([(cx, cy), (cx, cy + dy * corner_size)], fill=accent_color, width=3)

    # Center placement
    cx, cy = width // 2, height // 2

    # Draw diamond accent
    diamond_size = 14
    draw.polygon(
        [
            (cx, cy - 80 - diamond_size),
            (cx + diamond_size, cy - 80),
            (cx, cy - 80 + diamond_size),
            (cx - diamond_size, cy - 80),
        ],
        outline=accent_color,
        fill=None
    )

    # Font setup fallback
    try:
        font_sub = ImageFont.load_default()
        font_main = ImageFont.load_default()
    except Exception:
        font_sub = None
        font_main = None

    # Draw Subtitle (e.g. "COCO HOTEL")
    draw.text((cx, cy - 40), subtitle.upper(), fill=accent_color, anchor="mm", font=font_sub)

    # Draw Title (e.g. "Deluxe Queen Room")
    draw.text((cx, cy + 10), title, fill=(245, 245, 240), anchor="mm", font=font_main)

    # Bottom subtle hospitality line
    draw.text((cx, cy + 60), "BOUTIQUE HOSPITALITY & TRANQUILITY", fill=(140, 130, 120), anchor="mm", font=font_sub)

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=90)
    return buffer.getvalue()


class Command(BaseCommand):
    help = "Deterministically seeds Neon DEV with realistic multilingual Coco Hotel showcase data and luxury mock assets."

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm-dev',
            action='store_true',
            help='Explicit confirmation that this command is running in a DEV environment.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # 1. Safety Checks
        dev_seed_allowed = os.environ.get("DEV_SEED_ALLOWED", "").strip().lower() in ("true", "1", "yes")
        if not dev_seed_allowed:
            raise CommandError("DEV seeding is refused. Set DEV_SEED_ALLOWED=True in environment (backend/.env).")

        if not options.get('confirm_dev'):
            raise CommandError("Refusing to seed without explicit --confirm-dev confirmation flag.")

        self.stdout.write(self.style.NOTICE("--- Starting Coco Hotel Multilingual DEV Showcase Data Seeding ---"))

        # 2. Hotel Information (Singleton)
        hotel_info = HotelInformation.objects.first()
        if not hotel_info:
            hotel_info = HotelInformation.objects.create(
                name="Coco Hotel",
                hero_title="An Intimate Sanctuary in the Heart of the City",
                hero_title_en="An Intimate Sanctuary in the Heart of the City",
                hero_title_uz="Shahar markazidagi sokin va qulay maskan",
                hero_title_ru="Уединенное убежище в самом сердце города",
                hero_subtitle="Refined comfort, timeless architecture, and personalized hospitality crafted for the discerning traveler.",
                hero_subtitle_en="Refined comfort, timeless architecture, and personalized hospitality crafted for the discerning traveler.",
                hero_subtitle_uz="Nozik did bilan yaratilgan qulaylik, betakror arxitektura va har bir mehmon uchun individual e'tibor.",
                hero_subtitle_ru="Изысканный комфорт, неподвластная времени архитектура и индивидуальное гостеприимство для взыскательных путешественников.",
                about_title="Discreet Luxury, Thoughtful Design",
                about_title_en="Discreet Luxury, Thoughtful Design",
                about_title_uz="Vazmin hashamat, nozik didli dizayn",
                about_title_ru="Сдержанная роскошь, продуманный дизайн",
                about_text=(
                    "Coco Hotel offers an intimate retreat crafted with calm sophistication. "
                    "Every space balances peaceful natural tones, tactile materials, and bespoke craftsmanship with modern boutique standards. "
                    "We invite our guests to slow down, rest deeply, and experience hospitality rooted in warmth and authentic care."
                ),
                about_text_en=(
                    "Coco Hotel offers an intimate retreat crafted with calm sophistication. "
                    "Every space balances peaceful natural tones, tactile materials, and bespoke craftsmanship with modern boutique standards. "
                    "We invite our guests to slow down, rest deeply, and experience hospitality rooted in warmth and authentic care."
                ),
                about_text_uz=(
                    "Coco Hotel xotirjamlik va nafislik bilan yaratilgan shinam maskandir. "
                    "Har bir xona sokin tabiiy ohanglar, sifatli materiallar va zamonaviy butik-mehmonxona andozalari bilan uyg'unlashgan. "
                    "Biz mehmonlarimizni samimiy mehmondo'stlik va g'amxo'rlik muhitida dam olishga taklif etamiz."
                ),
                about_text_ru=(
                    "Coco Hotel — это уединенный бутик-отель, созданный в атмосфере спокойствия и изысканности. "
                    "Каждое пространство гармонично сочетает мягкие природные тона, натуральные материалы и современные стандарты гостеприимства. "
                    "Мы приглашаем наших гостей насладиться искренней заботой и безупречным уютом."
                ),
                phone="+998 71 200 4567",
                secondary_phone="+998 71 200 4568",
                email="concierge@cocohotel.com",
                address="45 Afrosiyob Street, Mirabad District, Tashkent 100015, Uzbekistan",
                address_en="45 Afrosiyob Street, Mirabad District, Tashkent 100015, Uzbekistan",
                address_uz="45 Afrosiyob ko'chasi, Mirobod tumani, Toshkent 100015, O'zbekiston",
                address_ru="ул. Афросиёб, 45, Мирабадский район, Ташкент 100015, Узбекистан",
                map_url="https://maps.google.com/?q=41.2995,69.2401",
                latitude=Decimal("41.299500"),
                longitude=Decimal("69.240100"),
                check_in_time=time(14, 0),
                check_out_time=time(12, 0),
            )
            self.stdout.write(self.style.SUCCESS("[OK] Created HotelInformation record with UZ/RU/EN content."))
        else:
            hotel_info.name = "Coco Hotel"
            hotel_info.hero_title = "An Intimate Sanctuary in the Heart of the City"
            hotel_info.hero_title_en = "An Intimate Sanctuary in the Heart of the City"
            hotel_info.hero_title_uz = "Shahar markazidagi sokin va qulay maskan"
            hotel_info.hero_title_ru = "Уединенное убежище в самом сердце города"
            hotel_info.hero_subtitle = "Refined comfort, timeless architecture, and personalized hospitality crafted for the discerning traveler."
            hotel_info.hero_subtitle_en = "Refined comfort, timeless architecture, and personalized hospitality crafted for the discerning traveler."
            hotel_info.hero_subtitle_uz = "Nozik did bilan yaratilgan qulaylik, betakror arxitektura va har bir mehmon uchun individual e'tibor."
            hotel_info.hero_subtitle_ru = "Изысканный комфорт, неподвластная времени архитектура и индивидуальное гостеприимство для взыскательных путешественников."
            hotel_info.about_title = "Discreet Luxury, Thoughtful Design"
            hotel_info.about_title_en = "Discreet Luxury, Thoughtful Design"
            hotel_info.about_title_uz = "Vazmin hashamat, nozik didli dizayn"
            hotel_info.about_title_ru = "Сдержанная роскошь, продуманный дизайн"
            hotel_info.about_text = (
                "Coco Hotel offers an intimate retreat crafted with calm sophistication. "
                "Every space balances peaceful natural tones, tactile materials, and bespoke craftsmanship with modern boutique standards. "
                "We invite our guests to slow down, rest deeply, and experience hospitality rooted in warmth and authentic care."
            )
            hotel_info.about_text_en = hotel_info.about_text
            hotel_info.about_text_uz = (
                "Coco Hotel xotirjamlik va nafislik bilan yaratilgan shinam maskandir. "
                "Har bir xona sokin tabiiy ohanglar, sifatli materiallar va zamonaviy butik-mehmonxona andozalari bilan uyg'unlashgan. "
                "Biz mehmonlarimizni samimiy mehmondo'stlik va g'amxo'rlik muhitida dam olishga taklif etamiz."
            )
            hotel_info.about_text_ru = (
                "Coco Hotel — это уединенный бутик-отель, созданный в атмосфере спокойствия и изысканности. "
                "Каждое пространство гармонично сочетает мягкие природные тона, натуральные материалы и современные стандарты гостеприимства. "
                "Мы приглашаем наших гостей насладиться искренней заботой и безупречным уютом."
            )
            hotel_info.phone = "+998 71 200 4567"
            hotel_info.secondary_phone = "+998 71 200 4568"
            hotel_info.email = "concierge@cocohotel.com"
            hotel_info.address = "45 Afrosiyob Street, Mirabad District, Tashkent 100015, Uzbekistan"
            hotel_info.address_en = "45 Afrosiyob Street, Mirabad District, Tashkent 100015, Uzbekistan"
            hotel_info.address_uz = "45 Afrosiyob ko'chasi, Mirobod tumani, Toshkent 100015, O'zbekiston"
            hotel_info.address_ru = "ул. Афросиёб, 45, Мирабадский район, Ташкент 100015, Узбекистан"
            hotel_info.map_url = "https://maps.google.com/?q=41.2995,69.2401"
            hotel_info.latitude = Decimal("41.299500")
            hotel_info.longitude = Decimal("69.240100")
            hotel_info.check_in_time = time(14, 0)
            hotel_info.check_out_time = time(12, 0)
            hotel_info.save()
            self.stdout.write(self.style.SUCCESS("[OK] Updated existing HotelInformation record with UZ/RU/EN content."))

        # 3. Amenities
        amenities_data = [
            {
                "name": "Wi-Fi",
                "name_en": "High-Speed Wi-Fi",
                "name_uz": "Tezkor Wi-Fi",
                "name_ru": "Скоростной Wi-Fi",
                "icon": "wifi",
                "sort_order": 1
            },
            {
                "name": "Breakfast",
                "name_en": "Artisan Breakfast",
                "name_uz": "Nonushta",
                "name_ru": "Завтрак",
                "icon": "coffee",
                "sort_order": 2
            },
            {
                "name": "Parking",
                "name_en": "Private Parking",
                "name_uz": "Maxsus avtoturargoh",
                "name_ru": "Охраняемая парковка",
                "icon": "car",
                "sort_order": 3
            },
            {
                "name": "Air Conditioning",
                "name_en": "Climate Control",
                "name_uz": "Konditsioner tizimi",
                "name_ru": "Климат-контроль",
                "icon": "wind",
                "sort_order": 4
            },
            {
                "name": "Daily Cleaning",
                "name_en": "Daily Housekeeping",
                "name_uz": "Kundalik tozalash",
                "name_ru": "Ежедневная уборка",
                "icon": "sparkles",
                "sort_order": 5
            },
            {
                "name": "24/7 Reception",
                "name_en": "24/7 Concierge",
                "name_uz": "24/7 Qabulxona",
                "name_ru": "Круглосуточная стойка",
                "icon": "shield",
                "sort_order": 6
            },
            {
                "name": "Private Bathroom",
                "name_en": "En-Suite Marble Bath",
                "name_uz": "Shaxsiy marmar hammom",
                "name_ru": "Собственная ванная",
                "icon": "bath",
                "sort_order": 7
            },
            {
                "name": "Smart TV",
                "name_en": "Smart Ultra HD TV",
                "name_uz": "Smart Ultra HD TV",
                "name_ru": "Смарт-ТВ Ultra HD",
                "icon": "tv",
                "sort_order": 8
            },
            {
                "name": "Mini Bar",
                "name_en": "Curated Mini Bar",
                "name_uz": "Tanlangan mini-bar",
                "name_ru": "Мини-бар",
                "icon": "glass",
                "sort_order": 9
            },
            {
                "name": "Work Desk",
                "name_en": "Executive Work Desk",
                "name_uz": "Qulay ish stoli",
                "name_ru": "Письменный стол",
                "icon": "desk",
                "sort_order": 10
            },
        ]

        amenity_objs = {}
        for a_data in amenities_data:
            amenity, _ = Amenity.objects.update_or_create(
                name=a_data["name"],
                defaults={
                    "name_en": a_data["name_en"],
                    "name_uz": a_data["name_uz"],
                    "name_ru": a_data["name_ru"],
                    "icon": a_data["icon"],
                    "sort_order": a_data["sort_order"],
                    "is_active": True,
                }
            )
            amenity_objs[a_data["name"]] = amenity
        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(amenity_objs)} Multilingual Amenities."))

        # 4. Approved Services Only (No Laundry, No Airport Transfer)
        services_data = [
            {
                "name": "Wi-Fi",
                "name_en": "High-Speed Wi-Fi",
                "name_uz": "Tezkor Wi-Fi",
                "name_ru": "Высокоскоростной Wi-Fi",
                "description": "Complimentary high-speed fiber internet coverage across all guest rooms, public lounge, and courtyard.",
                "description_en": "Complimentary high-speed fiber internet coverage across all guest rooms, public lounge, and courtyard.",
                "description_uz": "Barcha xonalar, mehmonlar zali va hovlida bepul va yuqori tezlikdagi simsiz internet.",
                "description_ru": "Бесплатный высокоскоростной оптоволоконный интернет на всей территории отеля и в номерах.",
                "icon": "wifi",
                "sort_order": 1
            },
            {
                "name": "Breakfast",
                "name_en": "Artisan Breakfast",
                "name_uz": "Mualliflik nonushtasi",
                "name_ru": "Авторский завтрак",
                "description": "Daily curated morning table featuring fresh local organic fruits, freshly baked breads, warm dishes, and artisan coffee.",
                "description_en": "Daily curated morning table featuring fresh local organic fruits, freshly baked breads, warm dishes, and artisan coffee.",
                "description_uz": "Yangi mevalar, issiq pishiriqlar, mazali taomlar va xushbo'y qahva bilan to'yimli ertalabki dasturxon.",
                "description_ru": "Ежедневный изысканный завтрак со свежими фруктами, горячей выпечкой и превосходным кофе.",
                "icon": "coffee",
                "sort_order": 2
            },
            {
                "name": "Parking",
                "name_en": "Private Parking",
                "name_uz": "Xavfsiz avtoturargoh",
                "name_ru": "Охраняемая парковка",
                "description": "Secure, private on-site parking accessible 24 hours a day for resident guests with round-the-clock surveillance.",
                "description_en": "Secure, private on-site parking accessible 24 hours a day for resident guests with round-the-clock surveillance.",
                "description_uz": "Mehmonlar uchun kechayu kunduz videokuzatuv ostidagi qulay va xavfsiz avtoturargoh.",
                "description_ru": "Круглосуточная охраняемая частная парковка на территории отеля для наших гостей.",
                "icon": "car",
                "sort_order": 3
            },
            {
                "name": "24/7 Reception",
                "name_en": "24/7 Concierge & Reception",
                "name_uz": "24/7 Qabulxona va konsyerj",
                "name_ru": "Круглосуточная стойка и консьерж",
                "description": "Warm, round-the-clock front desk team ready to assist with seamless check-in, local recommendations, and inquiries.",
                "description_en": "Warm, round-the-clock front desk team ready to assist with seamless check-in, local recommendations, and inquiries.",
                "description_uz": "Har qanday vaqtda sizga yordam berishga, ro'yxatga olishga va ma'lumot berishga tayyor mehmondo'st xodimlar.",
                "description_ru": "Приветливая команда портье и консьержа готова помочь вам в любое время суток.",
                "icon": "shield",
                "sort_order": 4
            },
            {
                "name": "Daily Cleaning",
                "name_en": "Daily Housekeeping",
                "name_uz": "Kundalik tozalash xizmati",
                "name_ru": "Ежедневная уборка номеров",
                "description": "Immaculate room servicing, evening turndown upon request, and premium linen care performed with quiet discretion.",
                "description_en": "Immaculate room servicing, evening turndown upon request, and premium linen care performed with quiet discretion.",
                "description_uz": "Xonangizni har kuni bekamu-ko'st tozalash, yangi sochiqlar va yuqori sifatli choyshablar.",
                "description_ru": "Безупречная чистота, ежедневная смена полотенец и заботливый уход за постельным бельем.",
                "icon": "sparkles",
                "sort_order": 5
            },
            {
                "name": "Air Conditioning",
                "name_en": "Individual Climate Control",
                "name_uz": "Individual iqlim nazorati",
                "name_ru": "Индивидуальный климат-контроль",
                "description": "Silent in-room climate control system ensuring a pleasant, custom temperature throughout all seasons.",
                "description_en": "Silent in-room climate control system ensuring a pleasant, custom temperature throughout all seasons.",
                "description_uz": "Yilning istalgan faslida xonada xotirjam va qulay haroratni ta'minlovchi shovqinsiz tizim.",
                "description_ru": "Бесшумная система кондиционирования для идеальной температуры в номере в любое время года.",
                "icon": "wind",
                "sort_order": 6
            },
        ]

        for s_data in services_data:
            Service.objects.update_or_create(
                name=s_data["name"],
                defaults={
                    "name_en": s_data["name_en"],
                    "name_uz": s_data["name_uz"],
                    "name_ru": s_data["name_ru"],
                    "description": s_data["description"],
                    "description_en": s_data["description_en"],
                    "description_uz": s_data["description_uz"],
                    "description_ru": s_data["description_ru"],
                    "icon": s_data["icon"],
                    "sort_order": s_data["sort_order"],
                    "is_active": True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(services_data)} Approved Multilingual Services."))

        # 5. Showcase Rooms
        rooms_data = [
            {
                "slug": "deluxe-queen-room",
                "name": "Deluxe Queen Room",
                "name_en": "Deluxe Queen Room",
                "name_uz": "Deluxe Queen xonasi",
                "name_ru": "Номер Делюкс с кроватью Queen",
                "short_description": "An intimate sanctuary featuring an artisan queen-size bed, acoustic soundproofing, and en-suite marble bath.",
                "short_description_en": "An intimate sanctuary featuring an artisan queen-size bed, acoustic soundproofing, and en-suite marble bath.",
                "short_description_uz": "Qulay queen-size krovat, sokin muhit va shaxsiy marmar hammomga ega nafis xona.",
                "short_description_ru": "Уютный номер с кроватью queen-size, превосходной шумоизоляцией и мраморной ванной комнатой.",
                "description": (
                    "Designed for thoughtful relaxation, the Deluxe Queen Room combines understated boutique luxury "
                    "with quiet serenity. Furnished with custom walnut millwork, tailored ambient lighting, fine Italian linen, "
                    "and a private marble bathroom equipped with rain shower and organic botanical amenities."
                ),
                "description_en": (
                    "Designed for thoughtful relaxation, the Deluxe Queen Room combines understated boutique luxury "
                    "with quiet serenity. Furnished with custom walnut millwork, tailored ambient lighting, fine Italian linen, "
                    "and a private marble bathroom equipped with rain shower and organic botanical amenities."
                ),
                "description_uz": (
                    "Chuqur hordiq chiqarish uchun mo'ljallangan Deluxe Queen xonasi vazmin hashamat va sokinlikni o'zida mujassam etadi. "
                    "Yong'oq yog'ochidan ishlangan mebellar, nozik yorug'lik, a'lo sifatli choyshablar va tropik dushli shaxsiy marmar hammom."
                ),
                "description_ru": (
                    "Созданный для уединенного отдыха, номер Делюкс Queen гармонично сочетает сдержанный комфорт и тишину. "
                    "Мебель из натурального ореха, мягкое освещение, постельное белье премиум-класса и мраморная ванная с тропическим душем."
                ),
                "price_per_night": Decimal("120.00"),
                "max_adults": 2,
                "max_children": 1,
                "bed_type": "1 Queen Bed",
                "bed_type_en": "1 Queen Bed",
                "bed_type_uz": "1 ta Queen krovat",
                "bed_type_ru": "1 кровать Queen-size",
                "room_size": Decimal("32.00"),
                "is_featured": True,
                "sort_order": 1,
                "amenities": ["Wi-Fi", "Breakfast", "Air Conditioning", "Daily Cleaning", "Smart TV", "Mini Bar", "Private Bathroom"]
            },
            {
                "slug": "executive-twin-room",
                "name": "Executive Twin Room",
                "name_en": "Executive Twin Room",
                "name_uz": "Executive Twin xonasi",
                "name_ru": "Номер Твин представительского класса",
                "short_description": "Two premium twin beds, dedicated ergonomic work space, and panoramic city-view windows.",
                "short_description_en": "Two premium twin beds, dedicated ergonomic work space, and panoramic city-view windows.",
                "short_description_uz": "Ikkita alohida qulay krovat, qulay ish stoli va shahar manzarasi ko'rinadigan katta derazalar.",
                "short_description_ru": "Две раздельные премиальные кровати, удобная рабочая зона и панорамные окна.",
                "description": (
                    "Ideal for colleagues or friends traveling together, the Executive Twin Room offers two generous twin beds "
                    "with pocket-sprung orthopedic mattresses. The spacious interior features a solid wood executive desk, "
                    "soundproofing, a curated espresso bar, and generous closet space."
                ),
                "description_en": (
                    "Ideal for colleagues or friends traveling together, the Executive Twin Room offers two generous twin beds "
                    "with pocket-sprung orthopedic mattresses. The spacious interior features a solid wood executive desk, "
                    "soundproofing, a curated espresso bar, and generous closet space."
                ),
                "description_uz": (
                    "Hamkorlar yoki do'stlar uchun ayni muddao bo'lgan Executive Twin xonasi ortopedik matrasli ikkita qulay krovatni taqdim etadi. "
                    "Keng xonada sifatli yog'och ish stoli, espresso burchagi va qulay shkaf mavjud."
                ),
                "description_ru": (
                    "Идеально подходит для коллег или друзей: две просторные односпальные кровати с ортопедическими матрасами, "
                    "удобный письменный стол, тишина для работы и эспрессо-станция."
                ),
                "price_per_night": Decimal("145.00"),
                "max_adults": 2,
                "max_children": 1,
                "bed_type": "2 Single Twin Beds",
                "bed_type_en": "2 Single Twin Beds",
                "bed_type_uz": "2 ta bir kishilik krovat",
                "bed_type_ru": "2 раздельные кровати",
                "room_size": Decimal("36.00"),
                "is_featured": True,
                "sort_order": 2,
                "amenities": ["Wi-Fi", "Breakfast", "Air Conditioning", "Daily Cleaning", "Work Desk", "Smart TV", "Private Bathroom"]
            },
            {
                "slug": "junior-suite",
                "name": "Junior Suite",
                "name_en": "Junior Suite",
                "name_uz": "Junior Suite lyuks xonasi",
                "name_ru": "Джуниор Сюит",
                "short_description": "Expansive suite featuring a separate lounge salon, king-size bed, and freestanding soaking tub.",
                "short_description_en": "Expansive suite featuring a separate lounge salon, king-size bed, and freestanding soaking tub.",
                "short_description_uz": "Alohida mehmonxona burchagi, ulkan king-size krovat va nafis vanna bilan jihozlangan keng lyuks.",
                "short_description_ru": "Просторный номер с отдельной гостиной зоной, кроватью king-size и ванной для релаксации.",
                "description": (
                    "The Junior Suite is an architectural statement of serene luxury. "
                    "A curated salon area with designer sofa and armchairs seamlessly connects to a lavish master bedroom. "
                    "The bathroom is a private spa retreat with dual vanities, walk-in monsoon shower, and deep freestanding tub."
                ),
                "description_en": (
                    "The Junior Suite is an architectural statement of serene luxury. "
                    "A curated salon area with designer sofa and armchairs seamlessly connects to a lavish master bedroom. "
                    "The bathroom is a private spa retreat with dual vanities, walk-in monsoon shower, and deep freestanding tub."
                ),
                "description_uz": (
                    "Junior Suite xonasi xotirjam hashamatning yorqin namunasidir. "
                    "Dizaynerlik yumshoq mebellari bilan jihozlangan yashash burchagi shohona yotoqxona bilan bog'langan. "
                    "Ikki kishilik rakovina va chuqur vannaga ega spa uslubidagi hammom."
                ),
                "description_ru": (
                    "Джуниор Сюит — это воплощение изысканности и пространства. Уютная гостиная зона с дизайнерскими креслами, "
                    "великолепная спальня с кроватью king-size и роскошная ванная комната с ванной и тропическим душем."
                ),
                "price_per_night": Decimal("195.00"),
                "max_adults": 2,
                "max_children": 1,
                "bed_type": "1 King Bed",
                "bed_type_en": "1 King Bed",
                "bed_type_uz": "1 ta katta King krovat",
                "bed_type_ru": "1 кровать King-size",
                "room_size": Decimal("48.00"),
                "is_featured": True,
                "sort_order": 3,
                "amenities": ["Wi-Fi", "Breakfast", "Parking", "Air Conditioning", "Daily Cleaning", "Smart TV", "Mini Bar", "Work Desk", "Private Bathroom"]
            },
            {
                "slug": "family-suite",
                "name": "Family Suite",
                "name_en": "Family Suite",
                "name_uz": "Oilaviy Suite xonasi",
                "name_ru": "Семейный Сюит",
                "short_description": "Generous multi-room suite accommodating up to three adults and two children with supreme privacy.",
                "short_description_en": "Generous multi-room suite accommodating up to three adults and two children with supreme privacy.",
                "short_description_uz": "Oila a'zolari uchun maxsus mo'ljallangan, keng va to'liq jihozlangan shinam ko'p xonali suit.",
                "short_description_ru": "Просторный семейный номер из нескольких комнат с повышенным уровнем комфорта для всей семьи.",
                "description": (
                    "Thoughtfully crafted for memorable family stays. Offers a master bedroom with king bed alongside "
                    "an adjoining secondary bedroom with twin beds. Includes two private bathrooms, generous wardrobe storage, "
                    "and child-friendly safety features without compromising boutique design."
                ),
                "description_en": (
                    "Thoughtfully crafted for memorable family stays. Offers a master bedroom with king bed alongside "
                    "an adjoining secondary bedroom with twin beds. Includes two private bathrooms, generous wardrobe storage, "
                    "and child-friendly safety features without compromising boutique design."
                ),
                "description_uz": (
                    "Oilaviy unutilmas dam olish uchun noziklik bilan yaratilgan. Katta yotoqxona va alohida ikki krovatli bolalar xonasi. "
                    "Ikkita mustaqil hammom, keng garderob va yuqori xavfsizlik darajasi."
                ),
                "description_ru": (
                    "Прекрасно продуман для семейных поездок: главная спальня с кроватью king-size и смежная комната с двумя раздельными кроватями. "
                    "Две ванные комнаты и максимум пространства для каждого гостя."
                ),
                "price_per_night": Decimal("260.00"),
                "max_adults": 3,
                "max_children": 2,
                "bed_type": "1 King Bed + 2 Twin Beds",
                "bed_type_en": "1 King Bed + 2 Twin Beds",
                "bed_type_uz": "1 ta King krovat + 2 ta bir kishilik krovat",
                "bed_type_ru": "1 кровать King-size + 2 раздельные кровати",
                "room_size": Decimal("62.00"),
                "is_featured": False,
                "sort_order": 4,
                "amenities": ["Wi-Fi", "Breakfast", "Parking", "Air Conditioning", "Daily Cleaning", "Smart TV", "Mini Bar", "Work Desk", "Private Bathroom"]
            },
            {
                "slug": "premium-king-room",
                "name": "Premium King Room",
                "name_en": "Premium King Room",
                "name_uz": "Premium King xonasi",
                "name_ru": "Премиум номер с кроватью King",
                "short_description": "Elevated corner room with private balcony, oversized king bed, and sunlit morning exposure.",
                "short_description_en": "Elevated corner room with private balcony, oversized king bed, and sunlit morning exposure.",
                "short_description_uz": "Shaxsiy balkon, katta king krovat va ertalabki quyosh nuri bilan yoritiladigan yuqori qavatdagi xona.",
                "short_description_ru": "Угловой номер повышенной комфортности с отдельным балконом и роскошной кроватью king-size.",
                "description": (
                    "Positioned on the highest guest floors, the Premium King Room features floor-to-ceiling glass doors opening "
                    "onto a private terrace overlooking the verdant residential quarter. Includes a bespoke bar counter, "
                    "deep armchairs for reading, and acoustic insulation."
                ),
                "description_en": (
                    "Positioned on the highest guest floors, the Premium King Room features floor-to-ceiling glass doors opening "
                    "onto a private terrace overlooking the verdant residential quarter. Includes a bespoke bar counter, "
                    "deep armchairs for reading, and acoustic insulation."
                ),
                "description_uz": (
                    "Mehmonxonaning yuqori qavatlarida joylashgan Premium King xonasi manzarali xususiy terassaga ochiladigan vitraj derazalarga ega. "
                    "Qulay bar stoli, mutolaa uchun yumshoq kreslo va a'lo darajadagi shovqinsizlik."
                ),
                "description_ru": (
                    "Расположенный на верхних этажах, номер Премиум King имеет панорамные окна и собственный балкон с видом на тихий квартал. "
                    "Оснащен зоной отдыха, барной стойкой и великолепной кроватью king-size."
                ),
                "price_per_night": Decimal("165.00"),
                "max_adults": 2,
                "max_children": 1,
                "bed_type": "1 King Bed",
                "bed_type_en": "1 King Bed",
                "bed_type_uz": "1 ta katta King krovat",
                "bed_type_ru": "1 кровать King-size",
                "room_size": Decimal("40.00"),
                "is_featured": False,
                "sort_order": 5,
                "amenities": ["Wi-Fi", "Breakfast", "Air Conditioning", "Daily Cleaning", "Smart TV", "Mini Bar", "Work Desk", "Private Bathroom"]
            },
        ]

        for r_data in rooms_data:
            room, created = Room.objects.update_or_create(
                slug=r_data["slug"],
                defaults={
                    "name": r_data["name"],
                    "name_en": r_data["name_en"],
                    "name_uz": r_data["name_uz"],
                    "name_ru": r_data["name_ru"],
                    "short_description": r_data["short_description"],
                    "short_description_en": r_data["short_description_en"],
                    "short_description_uz": r_data["short_description_uz"],
                    "short_description_ru": r_data["short_description_ru"],
                    "description": r_data["description"],
                    "description_en": r_data["description_en"],
                    "description_uz": r_data["description_uz"],
                    "description_ru": r_data["description_ru"],
                    "price_per_night": r_data["price_per_night"],
                    "max_adults": r_data["max_adults"],
                    "max_children": r_data["max_children"],
                    "bed_type": r_data["bed_type"],
                    "bed_type_en": r_data["bed_type_en"],
                    "bed_type_uz": r_data["bed_type_uz"],
                    "bed_type_ru": r_data["bed_type_ru"],
                    "room_size": r_data["room_size"],
                    "is_featured": r_data["is_featured"],
                    "is_active": True,
                    "sort_order": r_data["sort_order"],
                }
            )

            # Assign amenities
            for a_name in r_data["amenities"]:
                if a_name in amenity_objs:
                    room.amenities.add(amenity_objs[a_name])

            # Seed 2 programmatic mock images per room if not already populated
            if room.images.count() == 0:
                # 1. Primary Image
                primary_bytes = create_luxury_placeholder_image(f"{r_data['name']} — Suite View", subtitle="COCO HOTEL RESIDENCES")
                p_file = ContentFile(primary_bytes, name=f"{r_data['slug']}-1.jpg")
                RoomImage.objects.create(
                    room=room,
                    image=p_file,
                    alt_text=f"{r_data['name']} primary interior view",
                    is_primary=True,
                    sort_order=1
                )

                # 2. Secondary Image
                secondary_bytes = create_luxury_placeholder_image(f"{r_data['name']} — Bath & Details", subtitle="COCO HOTEL RESIDENCES")
                s_file = ContentFile(secondary_bytes, name=f"{r_data['slug']}-2.jpg")
                RoomImage.objects.create(
                    room=room,
                    image=s_file,
                    alt_text=f"{r_data['name']} detail perspective",
                    is_primary=False,
                    sort_order=2
                )

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(rooms_data)} Multilingual Showcase Rooms with images."))

        # 6. Gallery Entries
        gallery_items = [
            {
                "title": "Grand Lobby & Lounge",
                "title_en": "Grand Lobby & Lounge",
                "title_uz": "Bosh qabulxona va mehmonlar zali",
                "title_ru": "Главный холл и лаундж",
                "alt_text": "Warm architectural lounge with textured stone and contemporary furnishings",
                "alt_text_en": "Warm architectural lounge with textured stone and contemporary furnishings",
                "alt_text_uz": "Tabiiy tosh va zamonaviy mebellar bilan bezatilgan shinam zal",
                "alt_text_ru": "Уютный лаундж отеля с отделкой из натурального камня и мягким светом",
                "file_name": "gallery-lobby.jpg",
                "sort_order": 1
            },
            {
                "title": "Deluxe Guest Suite",
                "title_en": "Deluxe Guest Suite",
                "title_uz": "Deluxe mehmon xonasi",
                "title_ru": "Номер Делюкс",
                "alt_text": "Minimalist guest suite with upholstered headboard and soft ambient lamps",
                "alt_text_en": "Minimalist guest suite with upholstered headboard and soft ambient lamps",
                "alt_text_uz": "Yumshoq yoritgichlar va qulay krovatli shinam mehmon xonasi",
                "alt_text_ru": "Стильный номер с мягким изголовьем кровати и рассеянным освещением",
                "file_name": "gallery-suite.jpg",
                "sort_order": 2
            },
            {
                "title": "Executive Suite Living Area",
                "title_en": "Executive Suite Living Area",
                "title_uz": "Executive Suite dam olish maydoni",
                "title_ru": "Гостиная зона представительского сюита",
                "alt_text": "Comfortable suite seating area with bespoke armchairs and low walnut coffee table",
                "alt_text_en": "Comfortable suite seating area with bespoke armchairs and low walnut coffee table",
                "alt_text_uz": "Maxsus kreslolar va yong'oq yog'ochidan ishlangan kofe stoli",
                "alt_text_ru": "Уютная зона отдыха с дизайнерскими креслами и журнальным столиком",
                "file_name": "gallery-living.jpg",
                "sort_order": 3
            },
            {
                "title": "Boutique Breakfast Room",
                "title_en": "Boutique Breakfast Room",
                "title_uz": "Nonushta zali",
                "title_ru": "Зал для завтраков",
                "alt_text": "Morning dining room featuring fresh seasonal pastries and sunlit table arrangements",
                "alt_text_en": "Morning dining room featuring fresh seasonal pastries and sunlit table arrangements",
                "alt_text_uz": "Ertalabki yorug' nonushta zali va yangi pishiriqlar",
                "alt_text_ru": "Светлый зал для завтраков со свежей выпечкой и сервировкой",
                "file_name": "gallery-breakfast.jpg",
                "sort_order": 4
            },
            {
                "title": "Evening Courtyard & Terrace",
                "title_en": "Evening Courtyard & Terrace",
                "title_uz": "Oqshomgi hovli va terassa",
                "title_ru": "Вечерний дворик и терраса",
                "alt_text": "Tranquil outdoor terrace illuminated by subtle path lanterns at dusk",
                "alt_text_en": "Tranquil outdoor terrace illuminated by subtle path lanterns at dusk",
                "alt_text_uz": "Kechki chiroqlar bilan yoritilgan sokin ochiq terassa",
                "alt_text_ru": "Уютная вечерняя терраса с приглушенной подсветкой",
                "file_name": "gallery-terrace.jpg",
                "sort_order": 5
            },
            {
                "title": "Artisan Espresso Bar",
                "title_en": "Artisan Espresso Bar",
                "title_uz": "Qahva burchagi",
                "title_ru": "Эспрессо-бар",
                "alt_text": "Polished granite coffee bar serving specialty freshly ground espresso drinks",
                "alt_text_en": "Polished granite coffee bar serving specialty freshly ground espresso drinks",
                "alt_text_uz": "Xushbo'y qahva va espresso tayyorlanadigan qulay bar",
                "alt_text_ru": "Барная стойка со свежесваренным кофе премиум-сортов",
                "file_name": "gallery-coffee.jpg",
                "sort_order": 6
            },
            {
                "title": "En-Suite Marble Bathroom",
                "title_en": "En-Suite Marble Bathroom",
                "title_uz": "Marmar hammom",
                "title_ru": "Мраморная ванная комната",
                "alt_text": "Monochrome marble bathroom with walk-in glass shower and dual rain heads",
                "alt_text_en": "Monochrome marble bathroom with walk-in glass shower and dual rain heads",
                "alt_text_uz": "Tropik dush va zamonaviy kranlar bilan jihozlangan marmar hammom",
                "alt_text_ru": "Ванная комната из натурального мрамора с душевой кабиной",
                "file_name": "gallery-bathroom.jpg",
                "sort_order": 7
            },
            {
                "title": "Private Meeting Room",
                "title_en": "Private Meeting Room",
                "title_uz": "Shaxsiy uchrashuvlar xonasi",
                "title_ru": "Переговорная комната",
                "alt_text": "Acoustically insulated meeting room for confidential executive discussions",
                "alt_text_en": "Acoustically insulated meeting room for confidential executive discussions",
                "alt_text_uz": "Muzokaralar va ishchan uchrashuvlar uchun mo'ljallangan tinch xona",
                "alt_text_ru": "Звукоизолированная комната для деловых встреч и переговоров",
                "file_name": "gallery-meeting.jpg",
                "sort_order": 8
            },
        ]

        for g_data in gallery_items:
            img_record = GalleryImage.objects.filter(title=g_data["title"]).first()
            if not img_record:
                img_bytes = create_luxury_placeholder_image(g_data["title"], subtitle="COCO HOTEL GALLERY")
                content_file = ContentFile(img_bytes, name=g_data["file_name"])
                GalleryImage.objects.create(
                    title=g_data["title"],
                    title_en=g_data["title_en"],
                    title_uz=g_data["title_uz"],
                    title_ru=g_data["title_ru"],
                    alt_text=g_data["alt_text"],
                    alt_text_en=g_data["alt_text_en"],
                    alt_text_uz=g_data["alt_text_uz"],
                    alt_text_ru=g_data["alt_text_ru"],
                    image=content_file,
                    sort_order=g_data["sort_order"],
                    is_active=True,
                )
            else:
                img_record.title_en = g_data["title_en"]
                img_record.title_uz = g_data["title_uz"]
                img_record.title_ru = g_data["title_ru"]
                img_record.alt_text = g_data["alt_text"]
                img_record.alt_text_en = g_data["alt_text_en"]
                img_record.alt_text_uz = g_data["alt_text_uz"]
                img_record.alt_text_ru = g_data["alt_text_ru"]
                img_record.sort_order = g_data["sort_order"]
                img_record.is_active = True
                img_record.save()
        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(gallery_items)} Multilingual Gallery Items."))

        # 7. Active Promotions
        promotions_data = [
            {
                "slug": "early-booking-offer",
                "title": "Early Booking Privileges",
                "title_en": "Early Booking Privileges",
                "title_uz": "Oldindan bron qilish imtiyozi",
                "title_ru": "Привилегии раннего бронирования",
                "short_description": "Reserve your stay at least 14 days in advance to enjoy daily complimentary artisan breakfast and flexible arrival.",
                "short_description_en": "Reserve your stay at least 14 days in advance to enjoy daily complimentary artisan breakfast and flexible arrival.",
                "short_description_uz": "Kamida 14 kun oldin xona buyurtma qiling va bepul nonushta hamda qulay kirish imkoniyatidan foydalaning.",
                "short_description_ru": "Забронируйте проживание минимум за 14 дней и получите комплиментарный авторский завтрак и гибкое время заезда.",
                "description": (
                    "Plan your journey ahead and secure preferred room selection with our Early Booking Privileges. "
                    "Guests booking a minimum of 14 days prior to arrival receive daily complimentary breakfast for up to two guests, "
                    "personalized arrival tea service, and priority consideration for early check-in subject to room availability."
                ),
                "description_en": (
                    "Plan your journey ahead and secure preferred room selection with our Early Booking Privileges. "
                    "Guests booking a minimum of 14 days prior to arrival receive daily complimentary breakfast for up to two guests, "
                    "personalized arrival tea service, and priority consideration for early check-in subject to room availability."
                ),
                "description_uz": (
                    "Sayohat rejangizni oldindan tuzing va eng yaxshi xonalarni qulay shartlar bilan bron qiling. "
                    "14 kun oldin band qilgan mehmonlar uchun 2 kishilik bepul nonushta, xush kelibsiz choyi va imkoniyatga qarab erta kirish taqdim etiladi."
                ),
                "description_ru": (
                    "Спланируйте визит заранее и выберите лучшие номера отеля. "
                    "При бронировании за 14 дней до заезда гостям предоставляется бесплатный завтрак на двоих, приветственный чайный сет и приоритетный ранний заезд при наличии номеров."
                ),
                "valid_from": date.today() - timedelta(days=7),
                "valid_until": date.today() + timedelta(days=90),
                "sort_order": 1,
                "file_name": "promotion-early-booking.jpg"
            },
            {
                "slug": "weekend-stay-offer",
                "title": "Weekend Retreat Experience",
                "title_en": "Weekend Retreat Experience",
                "title_uz": "Dam olish kunlari maxsus taklifi",
                "title_ru": "Выходные дни в Coco Hotel",
                "short_description": "Unwind over the weekend with extended 15:00 late check-out, afternoon welcome tea, and calm boutique atmosphere.",
                "short_description_en": "Unwind over the weekend with extended 15:00 late check-out, afternoon welcome tea, and calm boutique atmosphere.",
                "short_description_uz": "Dam olish kunlarini soat 15:00 gacha uzaytirilgan chiqish va xushbo'y choy xizmati bilan xotirjam o'tkazing.",
                "short_description_ru": "Проведите выходные в спокойной атмосфере с поздним выездом до 15:00 и приветственным чайным ритуалом.",
                "description": (
                    "Designed for city residents and weekend visitors seeking peaceful respite. "
                    "Enjoy late departure until 15:00 on Sunday, a welcome pot of organic local green tea served in your room upon arrival, "
                    "and a peaceful unhurried stay in the quietest quarter of Tashkent."
                ),
                "description_en": (
                    "Designed for city residents and weekend visitors seeking peaceful respite. "
                    "Enjoy late departure until 15:00 on Sunday, a welcome pot of organic local green tea served in your room upon arrival, "
                    "and a peaceful unhurried stay in the quietest quarter of Tashkent."
                ),
                "description_uz": (
                    "Shahar shovqinidan dam olmoqchi bo'lganlar uchun ajoyib imkoniyat. "
                    "Yakshanba kuni soat 15:00 gacha kechiktirilgan chiqish, xonaga yetkaziladigan tabiiy ko'k choy va to'liq sokinlik."
                ),
                "description_ru": (
                    "Предложение для тех, кто ищет уединения и перезагрузки на выходных. "
                    "Поздний выезд до 15:00, подача натурального чая в номер по прибытии и неспешный отдых в тихом уголке Ташкента."
                ),
                "valid_from": date.today() - timedelta(days=3),
                "valid_until": date.today() + timedelta(days=60),
                "sort_order": 2,
                "file_name": "promotion-weekend-retreat.jpg"
            },
        ]

        for p_data in promotions_data:
            promo = Promotion.objects.filter(slug=p_data["slug"]).first()
            if not promo:
                promo_bytes = create_luxury_placeholder_image(p_data["title"], subtitle="COCO HOTEL PRIVILEGES")
                p_file = ContentFile(promo_bytes, name=p_data["file_name"])
                Promotion.objects.create(
                    slug=p_data["slug"],
                    title=p_data["title"],
                    title_en=p_data["title_en"],
                    title_uz=p_data["title_uz"],
                    title_ru=p_data["title_ru"],
                    short_description=p_data["short_description"],
                    short_description_en=p_data["short_description_en"],
                    short_description_uz=p_data["short_description_uz"],
                    short_description_ru=p_data["short_description_ru"],
                    description=p_data["description"],
                    description_en=p_data["description_en"],
                    description_uz=p_data["description_uz"],
                    description_ru=p_data["description_ru"],
                    image=p_file,
                    valid_from=p_data["valid_from"],
                    valid_until=p_data["valid_until"],
                    is_active=True,
                    sort_order=p_data["sort_order"],
                )
            else:
                promo.title = p_data["title"]
                promo.title_en = p_data["title_en"]
                promo.title_uz = p_data["title_uz"]
                promo.title_ru = p_data["title_ru"]
                promo.short_description = p_data["short_description"]
                promo.short_description_en = p_data["short_description_en"]
                promo.short_description_uz = p_data["short_description_uz"]
                promo.short_description_ru = p_data["short_description_ru"]
                promo.description = p_data["description"]
                promo.description_en = p_data["description_en"]
                promo.description_uz = p_data["description_uz"]
                promo.description_ru = p_data["description_ru"]
                promo.valid_from = p_data["valid_from"]
                promo.valid_until = p_data["valid_until"]
                promo.sort_order = p_data["sort_order"]
                promo.is_active = True
                promo.save()
        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(promotions_data)} Multilingual Active Promotions."))

        self.stdout.write(self.style.SUCCESS("--- Multilingual DEV Showcase Data Seeding Completed Successfully ---"))
