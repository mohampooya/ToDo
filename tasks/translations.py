from django import template
#from .translations import translate_to_persian
# translations.py

# Example translation dictionary
translation_dict = {
  "hello": "سلام",
    "world": "دنیا",
    "username": "نام کاربری",
    "email": "ایمیل",
    "password1": "رمز عبور",
    "password2": "تکرار رمز عبور",
}

# Function to translate text from English to Persian
def translate_to_persian(text):
    words = text.split()
    translated_words = [translation_dict[(word.lower(), word) for word in words]]
    return ' '.join(translated_words)
register = template.Library()

@register.filter(name='translate_to_persian')
def translate_to_persian_filter(value):
    return translate_to_persian(value)
