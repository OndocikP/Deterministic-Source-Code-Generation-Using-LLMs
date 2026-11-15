import os
import random
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types



_FENCED_CODE_BLOCK_RE = re.compile(
    r"```(?:[a-zA-Z0-9_+\-#.]+)?\s*\n(?P<code>[\s\S]*?)\n```",
    re.DOTALL,
)


def _load_api_keys() -> list[str]:
    keys: list[str] = []

    # Načítaj kľúče zo súboru gemini_apikeys.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    apikeys_file = os.path.join(script_dir, "gemini_apikeys.txt")
    
    if not os.path.exists(apikeys_file):
        raise FileNotFoundError(
            f"Súbor {apikeys_file} neexistuje. "
            "Vytvor gemini_apikeys.txt s API kľúčmi (jeden kľúč na riadok)."
        )
    
    try:
        with open(apikeys_file, "r", encoding="utf-8") as f:
            for line in f:
                normalized = line.strip()
                if normalized and normalized not in keys:
                    keys.append(normalized)
    except Exception as e:
        raise RuntimeError(f"Chyba pri čítaní gemini_apikeys.txt: {e}") from e

    if not keys:
        raise ValueError(
            "Súbor gemini_apikeys.txt je prázdny. "
            "Pridaj API kľúče (jeden kľúč na riadok)."
        )

    return keys


API_KEYS = _load_api_keys()


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

    remaining_keys = API_KEYS.copy()

    max_retries = min(max_retries, len(API_KEYS))

    for attempt in range(1, max_retries + 1):
        if not remaining_keys:
            remaining_keys = API_KEYS.copy()

        selected_key = random.choice(remaining_keys)
        remaining_keys.remove(selected_key)

        client = genai.Client(api_key=selected_key)
        chat = client.chats.create(model=model, config=config)

        try:
            response = chat.send_message(prompt)
            code = _normalize_model_output(response.text or "")

            if not code:
                raise RuntimeError("Model vrátil prázdnu odpoveď.")

            #print(code)
            return code
        except errors.APIError as exc:
            status_code = getattr(exc, "status_code", None)
            retryable = status_code in {None, 429, 500, 502, 503, 504}

            if attempt == max_retries:
                raise RuntimeError(
                    f"Gemini API zlyhalo (status: {status_code}) po {max_retries} pokusoch."
                ) from exc

            delay = (base_retry_delay * (2 ** (attempt - 1))) if retryable else 1.0
            print(
                f"Gemini API je dočasne nedostupné (status: {status_code}). "
                f"Skúšam iný API kľúč, pokus {attempt}/{max_retries} za {delay:.1f}s..."
            )
            time.sleep(delay)
        except Exception as exc:
            if attempt == max_retries:
                raise RuntimeError(
                    f"Nepodarilo sa získať odpoveď od modelu po {max_retries} pokusoch."
                ) from exc

            delay = base_retry_delay * (2 ** (attempt - 1))
            print(
                "Model nevrátil použiteľnú odpoveď. "
                f"Skúšam iný API kľúč, pokus {attempt}/{max_retries} za {delay:.1f}s..."
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
