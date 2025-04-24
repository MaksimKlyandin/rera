def get_current_language(browser) -> str:
    """
    Gets current language from rera_locale cookie
    Returns: language code ('en', 'ru' or 'el')
    """
    cookie = browser.get_cookie('rera_locale')
    language = cookie.get('value') if cookie else 'en'
    return language if language in ['en', 'ru', 'el'] else 'en'