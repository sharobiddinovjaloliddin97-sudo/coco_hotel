"""S3 writes with stable public Supabase URLs for hotel photography."""
from urllib.parse import quote
from django.conf import settings
from storages.backends.s3 import S3Storage


class SupabaseMediaStorage(S3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        return f"{settings.SUPABASE_PUBLIC_MEDIA_URL.rstrip('/')}/{quote(name.lstrip('/'), safe='/')}"
