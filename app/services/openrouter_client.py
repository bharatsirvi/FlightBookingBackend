import os
import requests
import logging

logger = logging.getLogger(__name__)

def query_openrouter(query: str) -> str:
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            logger.error("❌ OPENROUTER_API_KEY is not set in environment variables.")
            return "OpenRouter API key is missing."

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {"role": "user", "content": query}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ OpenRouter API request failed: {e}")
        return "Failed to get response from OpenRouter."

    except KeyError as e:
        logger.error(f"❌ Malformed response from OpenRouter: {e}")
        return "Unexpected response from OpenRouter."
