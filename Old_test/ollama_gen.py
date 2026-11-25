import json
import re
import time
import urllib.error
import urllib.request


OLLAMA_URL = "http://localhost:11434"

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
	model: str = "qwen3:8b",
	think: bool | None = None,
	temperature: float = 0.2,
	top_p: float | None = None,
	top_k: int | None = None,
	seed: int | None = None,
	max_output_tokens: int = 4096,
	stop_sequences: list[str] | None = None,
	max_retries: int = 5,
	base_retry_delay: float = 2.0,
	url: str = OLLAMA_URL,
) -> str:
	options: dict[str, int | float | list[str]] = {
		"temperature": temperature,
		"num_predict": max_output_tokens,
	}

	if top_p is not None:
		options["top_p"] = top_p
	if top_k is not None:
		options["top_k"] = top_k
	if seed is not None:
		options["seed"] = seed
	if stop_sequences:
		options["stop"] = stop_sequences

	payload = {
		"model": model,
		"stream": False,
		"messages": [
			{"role": "system", "content": _build_system_instruction(language)},
			{"role": "user", "content": prompt},
		],
		"options": options,
	}
	if think is not None:
		payload["think"] = think

	request = urllib.request.Request(
		f"{url}/api/chat",
		data=json.dumps(payload).encode("utf-8"),
		headers={"Content-Type": "application/json"},
		method="POST",
	)

	for attempt in range(1, max_retries + 1):
		try:
			with urllib.request.urlopen(request, timeout=240) as response:
				result = json.loads(response.read().decode("utf-8"))

			code = _normalize_model_output(result.get("message", {}).get("content") or "")
			if not code:
				raise RuntimeError("Model vrátil prázdnu odpoveď.")

			#print(code)
			return code

		except urllib.error.HTTPError as exc:
			retryable = exc.code in {429, 500, 502, 503, 504}
			if not retryable or attempt == max_retries:
				raise RuntimeError(
					f"Ollama API zlyhalo (status: {exc.code}). Skús to znovu neskôr."
				) from exc

			delay = base_retry_delay * (2 ** (attempt - 1))
			print(
				f"Ollama API je dočasne nedostupné (status: {exc.code}). "
				f"Opakujem pokus {attempt}/{max_retries} za {delay:.1f}s..."
			)
			time.sleep(delay)

		except urllib.error.URLError as exc:
			if attempt == max_retries:
				raise RuntimeError(
					"Cannot connect to Ollama. Ensure 'ollama serve' is running on localhost:11434."
				) from exc

			delay = base_retry_delay * (2 ** (attempt - 1))
			print(
				"Ollama server je dočasne nedostupný. "
				f"Opakujem pokus {attempt}/{max_retries} za {delay:.1f}s..."
			)
			time.sleep(delay)

	raise RuntimeError("Nepodarilo sa získať odpoveď od modelu po viacerých pokusoch.")


#if __name__ == "__main__":
	# Príklad
	#code = generate_code(
	#	prompt="Vytvor Python REST API pomocou FastAPI s endpointom /users",
	#	language="Python",
	#	model="qwen2.5-coder:14b",
	#	temperature=0,
	#	top_p=1,
	#	top_k=40,
	#	seed=0,
	#	max_output_tokens=5000,
	#)
