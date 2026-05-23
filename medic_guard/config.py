from dotenv import load_dotenv
import os

def load_config() -> dict:
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "MODEL_NAME": os.getenv("MODEL_NAME", "gpt-4o"),
    }

if __name__ == "__main__":
    cfg = load_config()
    assert "MODEL_NAME" in cfg
    print("✅ Config loaded:", cfg["MODEL_NAME"])
