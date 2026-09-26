import os
from decimal import Decimal
from unittest import mock
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.language import get_request_language, parse_accept_language, resolve_multilingual_value
from hotel.models import HotelInformation, Service, GalleryImage, Promotion
from rooms.models import Amenity, Room


class LanguageHelperUnitTests(TestCase):
    """
    Unit tests for language parsing and multilingual field resolution.
    """

    def test_parse_accept_language_exact(self):
        self.assertEqual(parse_accept_language('uz'), 'uz')
        self.assertEqual(parse_accept_language('ru'), 'ru')
        self.assertEqual(parse_accept_language('en'), 'en')

    def test_parse_accept_language_locales(self):
        self.assertEqual(parse_accept_language('uz-UZ'), 'uz')
        self.assertEqual(parse_accept_language('ru-RU,ru;q=0.9'), 'ru')
        self.assertEqual(parse_accept_language('en-US,en;q=0.8'), 'en')

    def test_parse_accept_language_unsupported_and_empty(self):
        self.assertEqual(parse_accept_language(''), 'en')
        self.assertEqual(parse_accept_language(None), 'en')
        self.assertEqual(parse_accept_language('fr-FR,fr;q=0.9'), 'en')
        self.assertEqual(parse_accept_language('de,es;q=0.8'), 'en')

    def test_resolve_multilingual_value_fallback_hierarchy(self):
        class Dummy:
            name = "Legacy Title"
            name_en = "English Title"
            name_uz = "O'zbek Title"
            name_ru = "Русский Title"

        dummy = Dummy()
        # Direct language match
        self.assertEqual(resolve_multilingual_value(dummy, 'name', 'uz'), "O'zbek Title")
        self.assertEqual(resolve_multilingual_value(dummy, 'name', 'ru'), "Русский Title")
        self.assertEqual(resolve_multilingual_value(dummy, 'name', 'en'), "English Title")

        # Missing requested translation -> English fallback
        dummy.name_uz = ""
        self.assertEqual(resolve_multilingual_value(dummy, 'name', 'uz'), "English Title")

        # Missing English translation -> Legacy fallback
        dummy.name_en = ""
        self.assertEqual(resolve_multilingual_value(dummy, 'name', 'uz'), "Legacy Title")

        # Missing legacy -> First available non-empty
        dummy.name = ""
        self.assertEqual(resolve_multilingual_value(dummy, 'name', 'uz'), "Русский Title")

        # Empty all -> empty string
        dummy.name_ru = ""
        self.assertEqual(resolve_multilingual_value(dummy, 'name', 'uz'), "")


class MultilingualAPITests(APITestCase):
    """
    API integration tests verifying that public endpoints respect Accept-Language.
    """

    def setUp(self):
        self.amenity, _ = Amenity.objects.update_or_create(
            name="Wi-Fi",
            defaults={
                "name_en": "High-Speed Wi-Fi",
                "name_uz": "Tezkor Wi-Fi",
                "name_ru": "Скоростной Wi-Fi",
                "icon": "wifi",
                "sort_order": 1,
                "is_active": True,
            }
        )
        self.room, _ = Room.objects.update_or_create(
            slug="deluxe-suite-test",
            defaults={
                "name": "Deluxe Suite",
                "name_en": "Deluxe Suite EN",
                "name_uz": "Deluxe Suite UZ",
                "name_ru": "Делюкс Сюит RU",
                "short_description": "Short desc fallback",
                "short_description_en": "Short desc EN",
                "short_description_uz": "Qisqa tavsif UZ",
                "short_description_ru": "Краткое описание RU",
                "description": "Full desc fallback",
                "description_en": "Full desc EN",
                "description_uz": "Batafsil tavsif UZ",
                "description_ru": "Полное описание RU",
                "bed_type": "King Bed",
                "bed_type_en": "1 King Bed EN",
                "bed_type_uz": "1 ta King krovat UZ",
                "bed_type_ru": "1 кровать King RU",
                "price_per_night": Decimal("150.00"),
                "max_adults": 2,
                "max_children": 1,
                "is_active": True,
                "is_featured": True,
                "sort_order": 1,
            }
        )
        self.room.amenities.add(self.amenity)

        # Hotel Information
        hotel_info = HotelInformation.objects.first()
        if not hotel_info:
            self.hotel_info = HotelInformation.objects.create(
                name="Coco Hotel",
                hero_title="Sanctuary in the Heart",
                hero_title_en="Sanctuary in the Heart EN",
                hero_title_uz="Shahar markazidagi maskan UZ",
                hero_title_ru="Убежище в центре RU",
                hero_subtitle="Subtitle fallback",
                hero_subtitle_en="Subtitle EN",
                hero_subtitle_uz="Qo'shimcha tavsif UZ",
                hero_subtitle_ru="Подзаголовок RU",
                about_title="About Title fallback",
                about_title_en="About Title EN",
                about_title_uz="Biz haqimizda UZ",
                about_title_ru="Об отеле RU",
                about_text="About text fallback",
                about_text_en="About text EN",
                about_text_uz="Haqimizda matn UZ",
                about_text_ru="Текст об отеле RU",
                phone="+998712004567",
                email="info@example.com",
                address="Address fallback",
                address_en="Address EN",
                address_uz="Manzil UZ",
                address_ru="Адрес RU",
            )
        else:
            hotel_info.hero_title = "Sanctuary in the Heart"
            hotel_info.hero_title_en = "Sanctuary in the Heart EN"
            hotel_info.hero_title_uz = "Shahar markazidagi maskan UZ"
            hotel_info.hero_title_ru = "Убежище в центре RU"
            hotel_info.hero_subtitle = "Subtitle fallback"
            hotel_info.hero_subtitle_en = "Subtitle EN"
            hotel_info.hero_subtitle_uz = "Qo'shimcha tavsif UZ"
            hotel_info.hero_subtitle_ru = "Подзаголовок RU"
            hotel_info.about_title = "About Title fallback"
            hotel_info.about_title_en = "About Title EN"
            hotel_info.about_title_uz = "Biz haqimizda UZ"
            hotel_info.about_title_ru = "Об отеле RU"
            hotel_info.about_text = "About text fallback"
            hotel_info.about_text_en = "About text EN"
            hotel_info.about_text_uz = "Haqimizda matn UZ"
            hotel_info.about_text_ru = "Текст об отеле RU"
            hotel_info.address = "Address fallback"
            hotel_info.address_en = "Address EN"
            hotel_info.address_uz = "Manzil UZ"
            hotel_info.address_ru = "Адрес RU"
            hotel_info.save()
            self.hotel_info = hotel_info

        # Service
        self.service, _ = Service.objects.update_or_create(
            name="Breakfast",
            defaults={
                "name_en": "Breakfast EN",
                "name_uz": "Nonushta UZ",
                "name_ru": "Завтрак RU",
                "description": "Service desc fallback",
                "description_en": "Breakfast description EN",
                "description_uz": "Nonushta tavsifi UZ",
                "description_ru": "Описание завтрака RU",
                "icon": "coffee",
                "is_active": True,
                "sort_order": 1,
            }
        )

        # Promotion
        self.promotion, _ = Promotion.objects.update_or_create(
            slug="promo-multilingual",
            defaults={
                "title": "Promo fallback",
                "title_en": "Special Offer EN",
                "title_uz": "Maxsus taklif UZ",
                "title_ru": "Специальное предложение RU",
                "short_description": "Short fallback",
                "short_description_en": "Promo short EN",
                "short_description_uz": "Aksiya qisqa UZ",
                "short_description_ru": "Кратко об акции RU",
                "description": "Full promo fallback",
                "description_en": "Full promo EN",
                "description_uz": "Aksiya batafsil UZ",
                "description_ru": "Полные условия RU",
                "is_active": True,
                "sort_order": 1,
            }
        )

    def test_rooms_list_uzbek(self):
        url = reverse('rooms:room-list')
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='uz')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        room_data = results[0]
        self.assertEqual(room_data['name'], "Deluxe Suite UZ")
        self.assertEqual(room_data['short_description'], "Qisqa tavsif UZ")
        self.assertEqual(room_data['bed_type'], "1 ta King krovat UZ")
        self.assertEqual(room_data['amenities'][0]['name'], "Tezkor Wi-Fi")

    def test_rooms_list_russian(self):
        url = reverse('rooms:room-list')
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='ru-RU')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        room_data = results[0]
        self.assertEqual(room_data['name'], "Делюкс Сюит RU")
        self.assertEqual(room_data['short_description'], "Краткое описание RU")
        self.assertEqual(room_data['bed_type'], "1 кровать King RU")
        self.assertEqual(room_data['amenities'][0]['name'], "Скоростной Wi-Fi")

    def test_rooms_list_english_and_fallback(self):
        url = reverse('rooms:room-list')
        # Explicit English
        res_en = self.client.get(url, HTTP_ACCEPT_LANGUAGE='en-US')
        results_en = res_en.data.get('results', res_en.data) if isinstance(res_en.data, dict) else res_en.data
        self.assertEqual(results_en[0]['name'], "Deluxe Suite EN")
        # Unsupported language falls back to English
        res_de = self.client.get(url, HTTP_ACCEPT_LANGUAGE='de-DE')
        results_de = res_de.data.get('results', res_de.data) if isinstance(res_de.data, dict) else res_de.data
        self.assertEqual(results_de[0]['name'], "Deluxe Suite EN")

    def test_room_detail_multilingual(self):
        url = reverse('rooms:room-detail', kwargs={'slug': self.room.slug})
        # Uzbek
        res_uz = self.client.get(url, HTTP_ACCEPT_LANGUAGE='uz')
        self.assertEqual(res_uz.data['name'], "Deluxe Suite UZ")
        self.assertEqual(res_uz.data['description'], "Batafsil tavsif UZ")
        # Russian
        res_ru = self.client.get(url, HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(res_ru.data['name'], "Делюкс Сюит RU")
        self.assertEqual(res_ru.data['description'], "Полное описание RU")

    def test_hotel_information_multilingual(self):
        url = reverse('hotel:hotel-info')
        # Uzbek
        res_uz = self.client.get(url, HTTP_ACCEPT_LANGUAGE='uz')
        self.assertEqual(res_uz.data['hero_title'], "Shahar markazidagi maskan UZ")
        self.assertEqual(res_uz.data['about_title'], "Biz haqimizda UZ")
        self.assertEqual(res_uz.data['address'], "Manzil UZ")
        # Russian
        res_ru = self.client.get(url, HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(res_ru.data['hero_title'], "Убежище в центре RU")
        self.assertEqual(res_ru.data['about_title'], "Об отеле RU")
        self.assertEqual(res_ru.data['address'], "Адрес RU")

    def test_services_multilingual(self):
        url = reverse('hotel:service-list')
        res_uz = self.client.get(url, HTTP_ACCEPT_LANGUAGE='uz')
        self.assertEqual(res_uz.data[0]['name'], "Nonushta UZ")
        self.assertEqual(res_uz.data[0]['description'], "Nonushta tavsifi UZ")

        res_ru = self.client.get(url, HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(res_ru.data[0]['name'], "Завтрак RU")
        self.assertEqual(res_ru.data[0]['description'], "Описание завтрака RU")

    def test_promotions_multilingual(self):
        url = reverse('hotel:promotion-list')
        res_uz = self.client.get(url, HTTP_ACCEPT_LANGUAGE='uz')
        self.assertEqual(res_uz.data[0]['title'], "Maxsus taklif UZ")
        self.assertEqual(res_uz.data[0]['short_description'], "Aksiya qisqa UZ")

        res_ru = self.client.get(url, HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(res_ru.data[0]['title'], "Специальное предложение RU")
        self.assertEqual(res_ru.data[0]['short_description'], "Кратко об акции RU")


class SeedDevShowcaseCommandTests(TestCase):
    """
    Tests for the seed_dev_showcase management command safety guards and idempotency.
    """

    def test_refuses_without_confirm_dev_flag(self):
        with mock.patch.dict(os.environ, {"DEV_SEED_ALLOWED": "True"}):
            with self.assertRaises(CommandError) as cm:
                call_command('seed_dev_showcase')
            self.assertIn("--confirm-dev", str(cm.exception))

    def test_refuses_without_dev_seed_allowed_env(self):
        with mock.patch.dict(os.environ, {"DEV_SEED_ALLOWED": "False"}):
            with self.assertRaises(CommandError) as cm:
                call_command('seed_dev_showcase', confirm_dev=True)
            self.assertIn("DEV_SEED_ALLOWED", str(cm.exception))

    def test_seed_command_succeeds_and_is_idempotent(self):
        with mock.patch.dict(os.environ, {"DEV_SEED_ALLOWED": "True"}):
            # Run once
            call_command('seed_dev_showcase', confirm_dev=True)
            room_count_1 = Room.objects.count()
            amenity_count_1 = Amenity.objects.count()
            promo_count_1 = Promotion.objects.count()

            # Run again (must be idempotent, no duplicates)
            call_command('seed_dev_showcase', confirm_dev=True)
            self.assertEqual(Room.objects.count(), room_count_1)
            self.assertEqual(Amenity.objects.count(), amenity_count_1)
            self.assertEqual(Promotion.objects.count(), promo_count_1)
