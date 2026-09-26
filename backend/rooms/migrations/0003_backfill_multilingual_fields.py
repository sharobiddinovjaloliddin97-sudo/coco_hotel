from django.db import migrations


def backfill_rooms_multilingual_fields(apps, schema_editor):
    Room = apps.get_model('rooms', 'Room')
    Amenity = apps.get_model('rooms', 'Amenity')

    for amenity in Amenity.objects.all():
        if not amenity.name_en and amenity.name:
            amenity.name_en = amenity.name
            amenity.save(update_fields=['name_en'])

    for room in Room.objects.all():
        updated = []
        if not room.name_en and room.name:
            room.name_en = room.name
            updated.append('name_en')
        if not room.short_description_en and room.short_description:
            room.short_description_en = room.short_description
            updated.append('short_description_en')
        if not room.description_en and room.description:
            room.description_en = room.description
            updated.append('description_en')
        if not room.bed_type_en and room.bed_type:
            room.bed_type_en = room.bed_type
            updated.append('bed_type_en')
        if updated:
            room.save(update_fields=updated)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_amenity_name_en_amenity_name_ru_amenity_name_uz_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_rooms_multilingual_fields, reverse_code=noop),
    ]
