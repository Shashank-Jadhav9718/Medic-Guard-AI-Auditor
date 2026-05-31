import os
from dotenv import load_dotenv

# 1. Load environment variables from the workspace root .env file
root_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(root_env_path)

# 2. Enforce LangChain routing in NeMo Guardrails programmatically BEFORE importing NeMo
os.environ["NEMOGUARDRAILS_LLM_FRAMEWORK"] = "langchain"

# 3. Now import NeMo Guardrails (PEP 8 bypass for programmatic environment setup)
from nemoguardrails import LLMRails, RailsConfig  # noqa: E402


def get_rails() -> LLMRails:
    config = RailsConfig.from_path(os.path.dirname(__file__))
    return LLMRails(config)

if __name__ == "__main__":
    rails = get_rails()
    print("✅ NeMo Guardrails loaded:", type(rails).__name__)
