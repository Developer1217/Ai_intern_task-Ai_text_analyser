import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Payload(BaseModel):
    text: str


@app.post("/analyze")
def analyze_text(data: Payload):
    raw = data.text

    if not raw or not raw.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")

    words = re.findall(r"\b\w+\b", raw)
    word_count = len(words)
    char_count = len(raw)
    unique_count = len({w.lower() for w in words})

    sentences = [s for s in re.split(r"[.!?]+", raw) if s.strip()]
    sentence_count = len(sentences)

    total_chars = sum(len(w) for w in words)
    avg_len = round(total_chars / word_count, 2) if word_count > 0 else 0.0

    return {
        "word_count": word_count,
        "character_count": char_count,
        "unique_word_count": unique_count,
        "sentence_count": sentence_count,
        "average_word_length": avg_len,
        "uppercase_text": raw.upper(),
        "lowercase_text": raw.lower(),
    }