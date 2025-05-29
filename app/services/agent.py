
from app.services.lang_agent import ask_flight_agent

def llm_agent(user_query: str):
   
    response = ask_flight_agent(user_query)
    if response:
        return {**response}

    return {
        "type": "text",
        "description": "Sorry, I couldn't find an answer.",
        "source": "default"
    }
