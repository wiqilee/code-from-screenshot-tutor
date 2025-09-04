import argparse
from PIL import Image
from .ocr_engine import OcrEngine
from .lang_detect import detect_language
from .llm_backend import LLMBackend

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--mode", choices=["ocr","explain","refactor"], required=True)
    parser.add_argument("--language")
    args = parser.parse_args()

    img = Image.open(args.image).convert("RGB")
    res = OcrEngine().run(img)
    lang = args.language or detect_language(res.text)
    llm = LLMBackend()

    if args.mode == "ocr":
        print(res.text, "\nLang:", lang)
    elif args.mode == "explain":
        out = llm.generate(f"Explain this {lang} code:\n{res.text}")
        print(out)
    elif args.mode == "refactor":
        out = llm.generate(f"Refactor this {lang} code:\n{res.text}")
        print(out)

if __name__ == "__main__":
    main()
