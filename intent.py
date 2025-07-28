def get_intent(text: str) -> str:
    text = text.lower()
    if any(word in text for word in ["yes", "good", "happy", "great", "satisfied"]):
        return "positive"
    elif any(word in text for word in ["no", "bad", "unhappy", "late", "angry"]):
        return "negative"
    else:
        return "neutral"
