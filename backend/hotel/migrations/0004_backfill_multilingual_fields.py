from django.db import migrations


def backfill_hotel_multilingual_fields(apps, schema_editor):
    HotelInformation = apps.get_model('hotel', 'HotelInformation')
    Service = apps.get_model('hotel', 'Service')
    GalleryImage = apps.get_model('hotel', 'GalleryImage')
    Promotion = apps.get_model('hotel', 'Promotion')

    hotel_info = HotelInformation.objects.first()
    if hotel_info:
        updated = []
        if not hotel_info.hero_title_en and hotel_info.hero_title:
            hotel_info.hero_title_en = hotel_info.hero_title
            updated.append('hero_title_en')
        if not hotel_info.hero_subtitle_en and hotel_info.hero_subtitle:
            hotel_info.hero_subtitle_en = hotel_info.hero_subtitle
            updated.append('hero_subtitle_en')
        if not hotel_info.about_title_en and hotel_info.about_title:
            hotel_info.about_title_en = hotel_info.about_title
            updated.append('about_title_en')
        if not hotel_info.about_text_en and hotel_info.about_text:
            hotel_info.about_text_en = hotel_info.about_text
            updated.append('about_text_en')
        if not hotel_info.address_en and hotel_info.address:
            hotel_info.address_en = hotel_info.address
            updated.append('address_en')
        if updated:
            hotel_info.save(update_fields=updated)

    for service in Service.objects.all():
        updated = []
        if not service.name_en and service.name:
            service.name_en = service.name
            updated.append('name_en')
        if not service.description_en and service.description:
            service.description_en = service.description
            updated.append('description_en')
        if updated:
            service.save(update_fields=updated)

    for img in GalleryImage.objects.all():
        updated = []
        if not img.title_en and img.title:
            img.title_en = img.title
            updated.append('title_en')
        if not img.alt_text_en and img.alt_text:
            img.alt_text_en = img.alt_text
            updated.append('alt_text_en')
        if updated:
            img.save(update_fields=updated)

    for promo in Promotion.objects.all():
        updated = []
        if not promo.title_en and promo.title:
            promo.title_en = promo.title
            updated.append('title_en')
        if not promo.short_description_en and promo.short_description:
            promo.short_description_en = promo.short_description
            updated.append('short_description_en')
        if not promo.description_en and promo.description:
            promo.description_en = promo.description
            updated.append('description_en')
        if updated:
            promo.save(update_fields=updated)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_galleryimage_alt_text_en_galleryimage_alt_text_ru_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_hotel_multilingual_fields, reverse_code=noop),
    ]
