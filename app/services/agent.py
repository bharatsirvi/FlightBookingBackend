
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message here")
from app.services.lang_agent import ask_flight_agent

def llm_agent(user_query: str):
   
    lang_response = ask_flight_agent(user_query)
    if lang_response:
        return {**lang_response}

    return {
        "type": "text",
        "description": "Sorry, I couldn't find an answer.",
        "source": "default"
    }
