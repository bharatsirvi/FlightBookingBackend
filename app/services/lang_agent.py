from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_community.chat_models import ChatOpenAI
import pandas as pd
import os
from dotenv import load_dotenv
import re
import json
from langchain_core.output_parsers import JsonOutputParser
load_dotenv()

def create_flight_agent():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    bookings_path = os.path.normpath(os.path.join(current_dir, "..", "data", "flightbooking.csv"))
    bookings_df = pd.read_csv(bookings_path)

    mapping_path = os.path.normpath(os.path.join(current_dir, "..", "data", "airline_id_to_name.csv"))
    airline_mapping_df = pd.read_csv(mapping_path)

    bookings_df.rename(columns={"airlie_id": "airline_id"}, inplace=True)
    airline_mapping_df.rename(columns={"airlie_id": "airline_id"}, inplace=True)

    bookings_df["airline_id"] = bookings_df["airline_id"].astype(str)
    airline_mapping_df["airline_id"] = airline_mapping_df["airline_id"].astype(str)

    merged_df = bookings_df.merge(airline_mapping_df, on="airline_id", how="left")

    print("🔍 Sample merged rows:\n", merged_df.head())

    # LLM setup
    llm = ChatOpenAI(
        temperature=0,
        model="deepseek/deepseek-chat", 
        # model="deepseek/deepseek-chat:free",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1", 
    )

    return create_pandas_dataframe_agent(llm, merged_df, verbose=True, allow_dangerous_code=True,handle_parsing_errors=True, output_parser=JsonOutputParser())

# Create agent
flight_agent = create_flight_agent()

# Handle queries
def ask_flight_agent(query: str) -> dict:
   
   prompt = f"""
   You are a helpful data analyst.
   Use the given DataFrame to answer the following question.
   respond ONLY with a valid JSON object compatible with Highcharts (no markdown or extra text)
   1. For charts, use:
   {{
     "type": "chart",
     "chartType": "<pie|bar",
     "title": "<title of the chart>",
     "xAxis": [<list of categories for X-axis>],
     "yAxisTitle": "<title for Y-axis>",
     "series": [
       {{
         "name": "<series name>",
         "data": [list of list of x and y values, e.g. [[x1, y1], [x2, y2], ...]],>]
       }}
     ]
   }}

   2. For tables, use:
   {{
     "type": "table",
     "title": "<title>",
     "columns": ["col1", "col2", ...],
     "data": [
       ["row1val1", "row1val2", ...],
       ["row2val1", "row2val2", ...]
     ]
   }}

   3. For plain text:
   {{ "type": "text", "answer": "<summary>" }}

   4. If answer is not available:
   {{ "type": "text", "answer": "Sorry, I couldn't find an answer." }}

   give format that not give OUTPUT_PARSER_ERROR


   Question: {query}
   """


   raw_result = flight_agent.run(prompt)
   print("✅ Agent raw result:", raw_result)
   
   cleaned = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", raw_result, flags=re.DOTALL).strip()
   cleaned = cleaned.strip("`")
   cleaned = cleaned.replace("True", "true").replace("False", "false").replace("None", "null")
   print("🔍 Cleaned result:", cleaned)
   try:
        return json.loads(cleaned)
   except json.JSONDecodeError as e:
        return {"type": "text", "answer": "Sorry, I couldn't the response."}