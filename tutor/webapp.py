import gradio as gr
from PIL import Image
from .ocr_engine import OcrEngine
from .lang_detect import detect_language
from .llm_backend import LLMBackend

engine = OcrEngine()
llm = LLMBackend()

def process(image, mode, language):
    img = Image.fromarray(image)
    res = engine.run(img)
    lang = language or detect_language(res.text)
    if mode == "OCR":
        return res.text, lang, ""
    elif mode == "Explain":
        out = llm.generate(f"Explain this {lang} code step by step:\n{res.text}")
        return res.text, lang, out
    elif mode == "Refactor":
        out = llm.generate(f"Refactor this {lang} code with best practices:\n{res.text}")
        return res.text, lang, out

with gr.Blocks() as demo:
    gr.Markdown("# Code-from-Screenshot Tutor")
    with gr.Row():
        with gr.Column():
            image = gr.Image(type="numpy")
            mode = gr.Radio(["OCR","Explain","Refactor"], value="OCR")
            lang = gr.Textbox(label="Language (optional)")
            btn = gr.Button("Run")
        with gr.Column():
            ocr_box = gr.Textbox(label="OCR Text")
            lang_box = gr.Textbox(label="Language")
            out_box = gr.Textbox(label="Explanation / Refactor", lines=10)
    btn.click(process, inputs=[image, mode, lang], outputs=[ocr_box, lang_box, out_box])

def main():
    demo.launch(server_port=7861)

if __name__ == "__main__":
    main()
