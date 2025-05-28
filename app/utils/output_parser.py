from langchain.schema import BaseOutputParser
import re
import json

class JsonOutputParser(BaseOutputParser):
    def parse(self, text: str):
        
        cleaned = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", raw_result, flags=re.DOTALL).strip()
        cleaned = cleaned.strip("`")  # for cases with single backticks

    # Step 2: Replace Python-style literals with JSON-compatible ones
        cleaned = cleaned.replace("True", "true").replace("False", "false").replace("None", "null")
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON output: {e}")

    def get_format_instructions(self) -> str:
        return (
            "Respond ONLY with a valid JSON object compatible with Highcharts "
            "(no markdown or extra text)."
        )
