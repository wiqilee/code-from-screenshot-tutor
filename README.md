# Code-from-Screenshot Tutor

**By Wiqi Lee — Twitter: [@wiqi_lee](https://twitter.com/wiqi_lee)**  

An advanced toolkit that turns **code screenshots** into **clean code, explanations, refactors, and comparisons**.  
Supports both **OpenAI GPT models** and **local HuggingFace models** for flexible experimentation.

---

## ✨ Features
- 🖼️ OCR code extraction (EasyOCR)
- 🌐 Automatic language detection
- 🤖 LLM-powered explanations (OpenAI or local)
- 🛠️ Refactor with modern best practices
- 🔍 Compare two code screenshots side by side
- 📂 Export to `.py`, `.js`, `.cpp`
- ⚡ REST API, Gradio Web demo, and CLI

---

## 🚀 Quickstart

```bash
# 1. Setup virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run FastAPI backend
uvicorn tutor.api:app --reload --port 8010

# 4. Run Gradio web demo
python -m tutor.webapp
```

---

## 🔌 Endpoints

- `GET /health` → Health check  
- `POST /v1/ocr` → Extract code from screenshot  
- `POST /v1/explain` → Explain extracted code step by step  
- `POST /v1/refactor` → Refactor code with best practices  

---

## 📊 Example Workflows
1. Upload a screenshot of Python code → get OCR text.  
2. Use `/v1/explain` to receive detailed explanation from GPT-4o or TinyLlama.  
3. Use `/v1/refactor` to generate a cleaner, modernized version of the code.  
4. Compare outputs between OpenAI and HuggingFace backends.  

---

## 🏷️ Tech Stack
- Python 3.12+  
- [FastAPI](https://fastapi.tiangolo.com/) — API server  
- [Gradio](https://www.gradio.app/) — web UI  
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) — OCR engine  
- [Transformers](https://huggingface.co/transformers) — local models  
- [OpenAI](https://platform.openai.com/) — GPT integration  

---

## 📜 License
MIT License — feel free to fork, modify, and build upon.  
