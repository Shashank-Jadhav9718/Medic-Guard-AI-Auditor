from dotenv import load_dotenv
import os

def load_config() -> dict:
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
        "MODEL_NAME": os.getenv("MODEL_NAME", "gemini-2.5-flash"),
    }

if __name__ == "__main__":
    cfg = load_config()
    assert "MODEL_NAME" in cfg
    print("[OK] Config loaded:", cfg["MODEL_NAME"])
