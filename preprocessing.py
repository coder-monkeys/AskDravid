import re
import json


def clean_text(text: str) -> str:
    #TODO: this part will be improved as we test
    # Remove content in square brackets
    text = re.sub(r"\[.*?\]", "", text)

    # Remove emojis (basic unicode ranges)
    text = re.sub(r"[^\w\s.,!?'-]", "", text)

    # Normalize repeated punctuation
    text = re.sub(r"([!?.,])\1+", r"\1", text)

    # Lowercase
    text = text.lower()

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def clean_transcript(transcript):
    cleaned = []
    for entry in transcript:
        cleaned.append({
            "id": entry["id"],
            "text": clean_text(entry["text"]),
            "start": entry["start"],
            "end": entry["end"]
        })
    return cleaned



