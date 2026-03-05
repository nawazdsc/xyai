from config import RED_FLAGS

def check_red_flags(text):
    text = text.lower()
    return any(flag.lower() in text for flag in RED_FLAGS)
