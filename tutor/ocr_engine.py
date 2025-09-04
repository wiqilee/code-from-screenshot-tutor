# tutor/ocr_engine.py
from dataclasses import dataclass
from typing import List, Tuple
from PIL import Image
import numpy as np
import importlib

@dataclass
class OcrResult:
    text: str
    boxes: List[Tuple]

_READER = None  # cache singleton

def _get_reader(lang: str = "en"):
    global _READER
    if _READER is not None:
        return _READER
    # Lazy import to avoid heavy startup
    easyocr = importlib.import_module("easyocr")
    try:
        torch = importlib.import_module("torch")
        gpu = getattr(torch, "cuda", None) and torch.cuda.is_available()
    except Exception:
        gpu = False
    _READER = easyocr.Reader([lang], gpu=bool(gpu))
    return _READER

class OcrEngine:
    def __init__(self, lang: str = "en"):
        self.lang = lang

    def run(self, image: Image.Image) -> OcrResult:
        arr = np.array(image)
        reader = _get_reader(self.lang)
        results = reader.readtext(arr)
        text = "\n".join([r[1] for r in results])
        return OcrResult(text=text, boxes=[r[0] for r in results])
