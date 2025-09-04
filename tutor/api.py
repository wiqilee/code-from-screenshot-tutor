# tutor/api.py (potongan penting)
import io
from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from .lang_detect import detect_language
from .llm_backend import LLMBackend

app = FastAPI(title="Code-from-Screenshot Tutor")

def load_image(upload: UploadFile) -> Image.Image:
    return Image.open(io.BytesIO(upload.file.read())).convert("RGB")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/v1/ocr")
def ocr(image: UploadFile = File(...)):
    from .ocr_engine import OcrEngine  # lazy import
    img = load_image(image)
    res = OcrEngine().run(img)
    lang = detect_language(res.text)
    return {"ocr_text": res.text, "language": lang}

@app.post("/v1/explain")
def explain(image: UploadFile = File(...)):
    from .ocr_engine import OcrEngine  # lazy import
    img = load_image(image)
    res = OcrEngine().run(img)
    lang = detect_language(res.text)
    out = LLMBackend().generate(f"Explain this {lang} code step by step:\n{res.text}")
    return {"ocr_text": res.text, "language": lang, "explanation": out}

@app.post("/v1/refactor")
def refactor(image: UploadFile = File(...), language: str = Form(None)):
    from .ocr_engine import OcrEngine  # lazy import
    img = load_image(image)
    res = OcrEngine().run(img)
    lang = language or detect_language(res.text)
    out = LLMBackend().generate(f"Refactor this {lang} code with best practices:\n{res.text}")
    return {"ocr_text": res.text, "language": lang, "refactored": out}
