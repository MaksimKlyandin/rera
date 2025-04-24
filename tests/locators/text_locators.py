LOCALIZED_TEXT = {
    'en': {
        'next': 'Next',
        'location_step': 'Step 2/7 - Location',
        'select_location': 'Select location'
    },
    'ru': {
        'next': 'Далее',
        'location_step': 'Шаг 2/7 - Расположение',
        'select_location': 'Выберите расположение'
    },
    'el': {
        'next': 'Επόμενο',
        'location_step': 'Βήμα 2/7 - Τοποθεσία',
        'select_location': 'Επιλέξτε τοποθεσία'
    }
}

def get_localized_text(key: str, language: str) -> str:
    """
    Returns localized text for given key and language
    """
    return LOCALIZED_TEXT.get(language, {}).get(key, LOCALIZED_TEXT['en'][key])