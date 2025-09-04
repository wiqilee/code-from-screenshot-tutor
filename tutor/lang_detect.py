from pygments.lexers import guess_lexer

def detect_language(code: str) -> str:
    try:
        lexer = guess_lexer(code)
        return lexer.name.lower()
    except Exception:
        if "def " in code or "import " in code:
            return "python"
        if "#include" in code:
            return "cpp"
        if "function " in code:
            return "javascript"
        return "unknown"
