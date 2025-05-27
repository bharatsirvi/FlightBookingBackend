from app.services.basic_handler import basic_query_handler
from app.services.intermediate_handler import intermediate_query_handler
from app.utils.response_formatter import format_response  # Import your formatter

from app.services.openrouter_client import query_openrouter
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message here")
from app.services.lang_agent import ask_flight_agent

def llm_agent(user_query: str):
   
    lang_response = ask_flight_agent(user_query)
    if lang_response:
        return lang_response
    
    fallback_response = query_openrouter(user_query)
    return {
        "type": "text",
        "description": fallback_response,
        "source": "openrouter"
    }
