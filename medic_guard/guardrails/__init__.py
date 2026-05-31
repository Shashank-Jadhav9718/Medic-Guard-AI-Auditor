from nemoguardrails import LLMRails, RailsConfig
import os

def get_rails() -> LLMRails:
    config = RailsConfig.from_path(os.path.dirname(__file__))
    return LLMRails(config)

if __name__ == "__main__":
    rails = get_rails()
    print("✅ NeMo Guardrails loaded:", type(rails).__name__)
