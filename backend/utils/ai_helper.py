# ======================================================
# ai_helper.py - Gemini Wrapper + Smart JSON Parser
# Edumate v3 (Final Stable Fix 2.1)
# ======================================================
import os
import json
import re
import ast
from typing import Optional

try:
    import google.generativeai as genai
except Exception:
    genai = None


# ======================================================
# 🔹 Konfigurasi API
# ======================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_PRIORITY = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

if GEMINI_API_KEY and genai:
    genai.configure(api_key=GEMINI_API_KEY)


# ======================================================
# 🔹 Deteksi model terbaik
# ======================================================
def get_available_model():
    if not GEMINI_API_KEY or not genai:
        print("[AI INIT] ❌ API Key belum diatur.")
        return "gemini-1.5-flash"

    try:
        models = genai.list_models()
        model_names = [m.name for m in models]
        for pref in MODEL_PRIORITY:
            if any(pref in m for m in model_names):
                print(f"[AI INIT] ✅ Menggunakan model: {pref}")
                return pref
    except Exception as e:
        print(f"[AI INIT] ⚠️ Gagal cek model: {e}")
    return "gemini-1.5-flash"


MODEL_NAME = get_available_model()


# ======================================================
# 🔹 Fungsi generate teks dari Gemini (auto retry)
# ======================================================
def ask_gemini_raw(prompt: str, max_output_tokens: int = 2048, retries: int = 2) -> str:
    if not GEMINI_API_KEY or not genai:
        return "[AI Unavailable] API key / SDK error"

    for attempt in range(retries):
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_output_tokens}
            )
            text = getattr(response, "text", None)
            if text and len(text.strip()) > 0:
                return text.strip()
            print(f"[AI WARN] Output Gemini terpotong (retry {attempt+1}/{retries})...")
        except Exception as e:
            print(f"[AI Error] {e}")
    return ""


# ======================================================
# 🔹 Generate Chat Reply
# ======================================================
def generate_chat_reply(user_message: str, username: Optional[str] = None) -> str:
    ctx = (
        "Kamu adalah tutor AI yang ramah dan jelas. "
        "Jawab singkat, mudah dimengerti oleh siswa SMA. Berikan contoh jika perlu."
    )
    user_ctx = f"User: {username}" if username else ""
    prompt = f"{ctx}\n{user_ctx}\nPertanyaan: {user_message}\nJawab singkat:"
    return ask_gemini_raw(prompt, max_output_tokens=300)


# ======================================================
# 🔹 Generate Quiz Questions (AI) - FIXED VERSION
# ======================================================
def generate_quiz_questions(category: str, total: int = 30) -> str:
    prompt = (
        f"Buat {total} soal pilihan ganda tentang topik '{category}'.\n"
        "Formatkan dalam JSON array valid seperti ini:\n"
        "[\n"
        "  {\"q\": \"Pertanyaan...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"answer\": \"A\"}\n"
        "]\n"
        "Jangan sertakan penjelasan, kutipan kode, atau markdown seperti ```json. "
        "Pastikan JSON lengkap dan ditutup dengan benar."
    )
    return ask_gemini_raw(prompt, max_output_tokens=8192)


# ======================================================
# 🔹 JSON Parser Auto-Fix (Anti Fallback 2.0)
# ======================================================
def parse_possible_json(raw: str):
    """
    Parsing output Gemini jadi JSON valid.
    - Menghapus blok ```json dan teks non-JSON
    - Memperbaiki string yang belum tertutup
    - Menyelamatkan soal yang masih valid (anti fallback)
    """
    if not raw or not isinstance(raw, str):
        raise ValueError("Empty AI output")

    # Hilangkan blok kode markdown
    raw = re.sub(r"```json|```", "", raw, flags=re.IGNORECASE).strip()

    # Cari JSON array di dalam teks
    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON array found in AI output")

    json_str = raw[start:end + 1]

    # Bersihkan karakter aneh
    json_str = (
        json_str.replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\n", " ")
    )
    json_str = re.sub(r",\s*]", "]", json_str)
    json_str = re.sub(r",\s*}", "}", json_str)

    # ✅ Coba parse langsung
    try:
        parsed = json.loads(json_str)
        if isinstance(parsed, list) and all("q" in q for q in parsed):
            return parsed
    except Exception:
        pass

    # ✅ Jika gagal, coba potong manual
    fixed = []
    for match in re.finditer(r'\{[^{}]*\}', json_str):
        block = match.group()
        try:
            item = json.loads(block)
            if "q" in item and "options" in item and "answer" in item:
                fixed.append(item)
        except Exception:
            continue

    if fixed:
        print(f"[AI FIX] ✅ Berhasil selamatkan {len(fixed)} soal parsable.")
        return fixed

    print("[AI FAIL] ❌ Tidak ada soal valid, fallback dummy quiz.")
    return [
        {
            "q": f"[Fallback] Contoh soal 1 untuk topik umum. Pilih jawaban yang paling tepat.",
            "options": ["Pilihan A", "Pilihan B", "Pilihan C", "Pilihan D"],
            "answer": "A",
        }
    ]


# ======================================================
# 🔹 Helper (optional untuk debug)
# ======================================================
if __name__ == "__main__":
    # Tes lokal sederhana
    print("🔍 Tes generate quiz JSON:")
    sample = generate_quiz_questions("fisika dasar", 5)
    print(sample[:300], "...")
    parsed = parse_possible_json(sample)
    print(f"✅ Total soal valid: {len(parsed)}")


