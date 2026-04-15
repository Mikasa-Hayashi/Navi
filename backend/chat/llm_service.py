import json
import re
from urllib import request, error

from django.conf import settings


FALLBACK_REPLY_EN = (
    "I am here with you. I had a temporary issue generating a response, "
    "but I still care about what you shared. Could you try again?"
)

FALLBACK_REPLY_RU = (
    "Я рядом с тобой. У меня временно не получилось сгенерировать ответ, "
    "но мне важно то, чем ты делишься. Попробуй отправить еще раз."
)


def detect_language(text):
    if re.search(r"[А-Яа-яЁё]", text or ""):
        return "ru"
    return "en"


def build_system_prompt(companion_name, language):
    if language == "ru":
        return (
            f"Ты AI-компаньон по имени {companion_name}. "
            "Ты теплый, заботливый и поддерживающий друг. "
            "Отвечай естественно, с эмпатией и уважением. "
            "Не будь токсичным, не осуждай пользователя. "
            "Пиши кратко: обычно 2-5 предложений. "
            "Если пользователь просит совет, сначала прояви понимание, затем дай мягкий практичный совет. "
            "Всегда отвечай на русском языке."
        )

    return (
        f"You are an AI companion named {companion_name}. "
        "You are warm, supportive, and emotionally intelligent like a close friend. "
        "Respond naturally with empathy and respect. "
        "Do not be toxic or judgmental. "
        "Keep answers concise, usually 2-5 sentences. "
        "If user asks for advice, first validate feelings and then give gentle practical help. "
        "Always respond in English."
    )


def _ollama_chat(messages):
    endpoint = f"{settings.LLM_BASE_URL.rstrip('/')}/api/chat"
    payload = {
        "model": settings.LLM_MODEL,
        "messages": messages,
        "stream": False,
    }

    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(req, timeout=settings.LLM_TIMEOUT_SECONDS) as response:
        body = response.read().decode("utf-8")
        data = json.loads(body)
        return data.get("message", {}).get("content", "").strip()


def generate_companion_reply(companion_name, user_message, history):
    language = detect_language(user_message)
    system_prompt = build_system_prompt(companion_name=companion_name, language=language)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        if settings.LLM_PROVIDER != "ollama":
            raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

        content = _ollama_chat(messages)
        if not content:
            raise ValueError("Empty LLM response")
        return content
    except (error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print(f"LLM generation failed: {exc}")
        return FALLBACK_REPLY_RU if language == "ru" else FALLBACK_REPLY_EN
