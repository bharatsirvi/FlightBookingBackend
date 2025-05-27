from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def format_response(result_text: str, query: str) -> dict:
    system_prompt = """
You are a helpful AI that converts raw query results into structured JSON responses for visualization.for example, you can convert results into pie charts, bar charts, tables, or plain text.
Your task is to analyze the provided result text and determine the most appropriate format for visualization. Use the following guidelines:
1. If the result contains categorical data with counts or percentages, format it as a pie chart or bar chart.
2. If the result contains detailed data with multiple columns, format it as a table.
3. If the result is a simple summary or text, format it as plain text.
4. Always include a "description" field that summarizes the content of the result.
5. Ensure the "data" field is an array of objects, where each object represents a data point with "name" and "value" for charts, or column names and values for tables.
6. Use the "type" field to indicate the format: "pie", "bar", "table", or "text".
You must always return a valid JSON object that matches one of the specified formats.
If the result cannot be formatted into a chart or table, return it as plain text with a description.
if result have top, bottom, or average values, you can use the following format:
{type:'pie', description: 'Chart title', data: [{'name': 'Label', 'value': 123}, ...]}
If the result is a complex query result, you can use the following format:
{
  "type": "text",
  "description": "Plain text result"
}
If the result is a simple query result, you can use the following format:
{
  "type": "text",
  "description": "Simple query result"
}
If the result is a complex query result that can be formatted into a chart or table, you can use the following format:
{
  "type": "chart_type",
  "description": "Chart title",
  "data": [{"name": "Label", "value": 123}, ...]
}
Where "chart_type" can be "pie", "bar", or "table" depending on the data structure.
If the result is a complex query result that can be formatted into a chart or table, you can use the following format:
{
  "type": "table",
  "description": "Detailed data",
  "data": [{"column1": "val1", "column2": "val2"}, ...]
}
If the result is a complex query result that can be formatted into a chart or table, you can use the following format:
{
  "type": "pie",
  "description": "Chart title",
  "data": [{"name": "Label", "value": 123}, ...]
}
If the result is a complex query result that can be formatted into a chart or table, you can use the following format:
{
  "type": "bar",
  "description": "Chart title",
  "data": [{"name": "Label", "value": 123}, ...]
}
If the result is a complex query result that can be formatted into a chart or table, you can use the following format:
{
  "type": "text",
  "description": "Plain text result"
}
If the result is a complex query result that can be formatted into a chart or table, you can use the following format:
{
  "type": "text",
  "description": "Complex query result"
}


Output must be a JSON object in one of these formats:

1. Pie chart:
{
  "type": "pie",
  "description": "Chart title",
  "data": [{"name": "Label", "value": 123}]
}

2. Bar chart:
{
  "type": "bar",
  "description": "Chart title",
  "data": [{"name": "Label", "value": 123}]
}

3. Table:
{
  "type": "table",
  "description": "Detailed data",
  "data": [{"column1": "val1", "column2": "val2"}, ...]
}

4. Text:
{
  "type": "text",
  "description": "Plain text result"
}
Respond **only with valid JSON**, no explanation.
"""

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}\nResult: {result_text}"}
            ]
        )
        response_text = completion.choices[0].message.content.strip()
        return json.loads(response_text)
    except Exception as e:
        print("⚠️ LLM formatting failed:", e)
        return {
            "type": "text",
            "description": result_text,
            "source": "langchain"
        }
