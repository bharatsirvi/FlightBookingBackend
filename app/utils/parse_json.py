def parse_json_string(response_str: str) -> dict:
    import json
    try:
        return json.loads(response_str)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return {"type": "text", "description": response_str}
