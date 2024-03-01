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
    translated_words = [translation_dict.get(word.lower(), word) for word in words]
    return ' '.join(translated_words)
