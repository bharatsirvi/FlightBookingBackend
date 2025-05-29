

import re

def clean_json_response(raw_result: str) -> str:
    """
    Cleans LLM output to extract valid JSON:
    - Removes triple backticks/code blocks
    - Strips stray backticks
    - Converts Python literals to JSON
    - Extracts the largest JSON object if needed
    """
    # Remove triple backticks and optional 'json' after them
    cleaned = re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", raw_result, flags=re.DOTALL).strip()
    # Remove any remaining stray backticks
    cleaned = cleaned.strip("`")
    # Replace Python literals with JSON equivalents
    cleaned = cleaned.replace("True", "true").replace("False", "false").replace("None", "null")
    # Optionally, extract the largest JSON object if extra text remains
    json_match = re.search(r"\{[\s\S]+\}", cleaned)
    if json_match:
        cleaned = json_match.group(0)
    return cleaned