import os
from dotenv import load_dotenv

# 1. Load environment variables from the workspace root .env file
root_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(root_env_path)

# 2. Enforce LangChain routing in NeMo Guardrails programmatically
os.environ["NEMOGUARDRAILS_LLM_FRAMEWORK"] = "langchain"


def get_rails() -> "LLMRails":
    """Loads and initializes NeMo Guardrails with the local configuration.

    Returns:
        LLMRails: The initialized LLMRails guardrails instance.
    """
    from nemoguardrails import LLMRails, RailsConfig

    config = RailsConfig.from_path(os.path.dirname(__file__))
    return LLMRails(config)

if __name__ == "__main__":
    from nemoguardrails import LLMRails
    rails = get_rails()
    print("✅ NeMo Guardrails loaded:", type(rails).__name__)
