from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.config import settings

# Lazy loading: Only initialize LLM when API key is present
_llm_instance = None

def get_llm():
    """
    Get or create the LLM instance. Only initializes if GOOGLE_API_KEY is configured.
    Raises ValueError if API key is not set.
    """
    global _llm_instance
    
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is not configured. AI features require a valid Google API key.")
    
    if _llm_instance is None:
        _llm_instance = ChatGoogleGenerativeAI(
            google_api_key=settings.google_api_key,
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
    
    return _llm_instance

# For backwards compatibility, expose llm but it will be lazy-loaded
@property
def llm():
    return get_llm()