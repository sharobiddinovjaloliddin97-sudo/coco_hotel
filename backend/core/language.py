"""
Language selection and translation resolution helper for Coco Hotel backend.
Supports: Uzbek ('uz'), Russian ('ru'), English ('en').
"""

SUPPORTED_LANGUAGES = ('uz', 'ru', 'en')
DEFAULT_LANGUAGE = 'en'


def parse_accept_language(header_value):
    """
    Parse an HTTP Accept-Language header value and return the best matching supported language code.
    Accepts formats such as 'uz', 'ru', 'en', 'ru-RU', 'uz-UZ,uz;q=0.9,en;q=0.8', etc.
    Falls back to DEFAULT_LANGUAGE ('en').
    """
    if not header_value:
        return DEFAULT_LANGUAGE

    # Split by comma for multiple preference items
    parts = header_value.split(',')
    for part in parts:
        lang_range = part.split(';')[0].strip().lower()
        if not lang_range:
            continue
        primary = lang_range.split('-')[0].strip()
        if primary in SUPPORTED_LANGUAGES:
            return primary

    return DEFAULT_LANGUAGE


def get_request_language(request):
    """
    Determine the requested language from the request.
    Checks query parameter ?lang=... first, then HTTP_ACCEPT_LANGUAGE header.
    Defaults to 'en'.
    """
    if not request:
        return DEFAULT_LANGUAGE

    # Query param override if present
    query_lang = getattr(request, 'GET', {}).get('lang', '').strip().lower()
    if query_lang in SUPPORTED_LANGUAGES:
        return query_lang

    # Accept-Language header
    accept_lang = ''
    if hasattr(request, 'headers'):
        accept_lang = request.headers.get('Accept-Language', '')
    if not accept_lang and hasattr(request, 'META'):
        accept_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')

    return parse_accept_language(accept_lang)


def resolve_multilingual_value(instance, field_base_name, language):
    """
    Resolve a localized field value according to the following strict fallback order:
    1. requested language (f"{field_base_name}_{language}")
    2. English fallback (f"{field_base_name}_en")
    3. Legacy field value (getattr(instance, field_base_name, None))
    4. First non-empty translation among supported languages
    5. Empty string
    """
    if not instance:
        return ""

    # 1. Requested language
    lang_field = f"{field_base_name}_{language}"
    val = getattr(instance, lang_field, None)
    if val is not None and str(val).strip():
        return val

    # 2. English fallback
    if language != 'en':
        en_val = getattr(instance, f"{field_base_name}_en", None)
        if en_val is not None and str(en_val).strip():
            return en_val

    # 3. Legacy field
    legacy_val = getattr(instance, field_base_name, None)
    if legacy_val is not None and str(legacy_val).strip():
        return legacy_val

    # 4. First available non-empty translation
    for alt_lang in SUPPORTED_LANGUAGES:
        alt_val = getattr(instance, f"{field_base_name}_{alt_lang}", None)
        if alt_val is not None and str(alt_val).strip():
            return alt_val

    return ""
