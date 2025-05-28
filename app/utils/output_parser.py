from langchain.schema import BaseOutputParser
import re
import json

class JsonOutputParser(BaseOutputParser):
    def parse(self, text: str):
        # Remove markdown code blocks if any
        cleaned = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", text, flags=re.DOTALL).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON output: {e}")

    def get_format_instructions(self) -> str:
        return (
            "Respond ONLY with a valid JSON object compatible with Highcharts "
            "(no markdown or extra text)."
        )
