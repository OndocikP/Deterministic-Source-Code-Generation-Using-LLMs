import os
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types


# Načítanie .env
load_dotenv()

# API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY nie je nastavený v .env")


# Gemini client
client = genai.Client(api_key=api_key)

_FENCED_CODE_BLOCK_RE = re.compile(
    r"```(?:[a-zA-Z0-9_+\-#.]+)?\s*\n(?P<code>[\s\S]*?)\n```",
    re.DOTALL,
)


def _build_system_instruction(language: str) -> str:
    return f"""
You are a programming AI.

Always generate code based on the user's request.

Target programming language: {language}

Rules:
- Return only code.
- Do not explain the code.
- Do not use markdown code blocks.
- Do not write ```python or ```.
- Generate complete and working code whenever possible.
- Use only the target programming language: {language}.
""".strip()


def _normalize_model_output(text: str) -> str:
    cleaned = (text or "").strip()
    match = _FENCED_CODE_BLOCK_RE.search(cleaned)
    if match:
        return match.group("code").strip()

    return cleaned


def generate_code(
    prompt: str,
    language: str = "Python",
    model: str = "gemini-3.1-flash-lite",
    temperature: float = 0.2,
    top_p: float | None = None,
    top_k: int | None = None,
    seed: int | None = None,
    max_output_tokens: int = 4096,
    stop_sequences: list[str] | None = None,
    frequency_penalty: float | None = None,
    presence_penalty: float | None = None,
    max_retries: int = 5,
    base_retry_delay: float = 2.0,
) -> str:

    config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        seed=seed,
        max_output_tokens=max_output_tokens,
        stop_sequences=stop_sequences,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        system_instruction=_build_system_instruction(language),
    )

    chat = client.chats.create(model=model, config=config)

    for attempt in range(1, max_retries + 1):
        try:
            response = chat.send_message(prompt)
            code = _normalize_model_output(response.text or "")

            if not code:
                raise RuntimeError("Model vrátil prázdnu odpoveď.")

            #print(code)
            return code
        except errors.APIError as exc:
            status_code = getattr(exc, "status_code", None)
            retryable = status_code in {429, 500, 502, 503, 504}

            if not retryable or attempt == max_retries:
                raise RuntimeError(
                    f"Gemini API zlyhalo (status: {status_code}). Skús to znovu neskôr."
                ) from exc

            delay = base_retry_delay * (2 ** (attempt - 1))
            print(
                f"Gemini API je dočasne nedostupné (status: {status_code}). "
                f"Opakujem pokus {attempt}/{max_retries} za {delay:.1f}s..."
            )
            time.sleep(delay)

    raise RuntimeError("Nepodarilo sa získať odpoveď od modelu po viacerých pokusoch.")


#if __name__ == "__main__":
    # Príklad
    #code = generate_code(
    #    prompt="Vytvor Python REST API pomocou FastAPI s endpointom /users",
    #    language="Python",
    #    temperature=0,
    #    top_p=1,
    #    top_k=40,
    #    seed=0,
    #    max_output_tokens=5000,
    #    frequency_penalty=0.0,
    #    presence_penalty=0.0,
    #)
