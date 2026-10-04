"""Language-agnostic code generation that returns text without executing it."""

from __future__ import annotations

import os
import re


MODEL = os.environ.get("ARGUS_CODE_MODEL", "").strip() or "gemini-2.5-flash"
MAX_DESCRIPTION_CHARS = 8_000
MAX_CONSTRAINTS_CHARS = 2_000
MAX_OUTPUT_TOKENS = 8_192


def _get_api_key() -> str:
    from memory.config_manager import get_gemini_key

    key = get_gemini_key()
    if not key:
        raise ValueError("Gemini API key is not configured.")
    return key


def _clean_model_output(value: str) -> str:
    code = str(value or "").strip()
    match = re.fullmatch(r"(`{3,})[^\r\n]*\r?\n([\s\S]*?)\r?\n\1", code)
    if match:
        code = match.group(2).strip()
    if not code:
        raise ValueError("The model returned an empty code response.")
    return code


def _fenced_code(language: str, code: str) -> str:
    label = re.sub(r"[^A-Za-z0-9_+#.-]+", "-", language).strip("-")[:48] or "code"
    longest_backtick_run = max(
        (len(run) for run in re.findall(r"`+", code)),
        default=0,
    )
    fence = "`" * max(3, longest_backtick_run + 1)
    return f"{fence}{label}\n{code}\n{fence}"


def code_generator(parameters: dict | None = None) -> str:
    """Generate code for any requested language and return it as text only."""
    args = parameters or {}
    description = str(args.get("description") or "").strip()
    language = " ".join(str(args.get("language") or "Python").split())[:100]
    filename = " ".join(str(args.get("filename") or "").split())[:255]
    constraints = " ".join(str(args.get("constraints") or "").split())[:MAX_CONSTRAINTS_CHARS]

    if not description:
        return "Describe what the code should do."
    if len(description) > MAX_DESCRIPTION_CHARS:
        return f"Please keep the code request under {MAX_DESCRIPTION_CHARS} characters."

    filename_context = filename or "Choose a suitable source filename."
    constraints_context = constraints or "No additional version, platform, or framework constraints."
    prompt = f"""You are an experienced software developer.
Generate a complete, useful code answer in the exact requested language or dialect.
The requested language may be any programming language, query language, markup language, configuration language, or domain-specific language. If it is uncommon, use its own syntax and do not silently substitute another language.

Rules:
- Return source code only. Do not add explanations or Markdown fences.
- Include required imports, declarations, and sensible error handling.
- Follow the specified version, framework, platform, and filename when supplied.
- If the task requires multiple files, return each file with a clear filename comment and its contents in order.
- Do not claim the code was run, tested, or compiled.
- This tool only generates text; do not assume access to files, shell commands, or a runtime.

Requested language or dialect: {language}
Target filename: {filename_context}
Constraints: {constraints_context}

User's code request:
<code_request>
{description}
</code_request>

Source code:"""

    try:
        from google import genai

        client = genai.Client(api_key=_get_api_key())
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={"temperature": 0.2, "max_output_tokens": MAX_OUTPUT_TOKENS},
        )
        code = _clean_model_output(response.text)
        return _fenced_code(language, code)
    except Exception as exc:
        print(f"[CodeGenerator] Generation failed: {type(exc).__name__}: {exc}")
        return f"Could not generate code: {exc}"
