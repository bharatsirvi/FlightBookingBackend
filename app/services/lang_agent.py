from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_community.chat_models import ChatOpenAI
import pandas as pd
import os
from dotenv import load_dotenv
import re
import json
from app.utils.output_parser import JsonOutputParser


load_dotenv()

def create_flight_agent():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Load main flight data
    bookings_path = os.path.normpath(os.path.join(current_dir, "..", "data", "flightbooking.csv"))
    bookings_df = pd.read_csv(bookings_path)

    # Load airline ID-name mapping
    mapping_path = os.path.normpath(os.path.join(current_dir, "..", "data", "airline_id_to_name.csv"))
    airline_mapping_df = pd.read_csv(mapping_path)

    # Optional: Print column names for debugging
    print("📄 bookings_df columns:", bookings_df.columns.tolist())
    print("📄 airline_mapping_df columns:", airline_mapping_df.columns.tolist())

    # Ensure matching column names and same types
    bookings_df.rename(columns={"airlie_id": "airline_id"}, inplace=True)
    airline_mapping_df.rename(columns={"airlie_id": "airline_id"}, inplace=True)

    # Match data types
    bookings_df["airline_id"] = bookings_df["airline_id"].astype(str)
    airline_mapping_df["airline_id"] = airline_mapping_df["airline_id"].astype(str)

    # Merge on airline_id
    merged_df = bookings_df.merge(airline_mapping_df, on="airline_id", how="left")

    # Debug sample output
    print("🔍 Sample merged rows:\n", merged_df.head())

    # LLM setup
    llm = ChatOpenAI(
        temperature=0,
        model="deepseek/deepseek-chat", 
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1", 
    )

    return create_pandas_dataframe_agent(llm, merged_df, verbose=True, allow_dangerous_code=True,output_parser=JsonOutputParser(),)

# Create agent
flight_agent = create_flight_agent()

# Handle queries
def ask_flight_agent(query: str) -> dict:
   print("🧠 Agent received query:", query)
    

   prompt = f"""
   You are a helpful data analyst.
   Use the given DataFrame to answer the following question.

   Respond ONLY in JSON format compatible with Highcharts:
   {{
     "chartType": "<column|line|bar|pie>",
     "title": "<title of the chart>",
     "xAxis": [<list of categories for X-axis>],
     "yAxisTitle": "<title for Y-axis>",
     "series": [
       {{
         "name": "<series name>",
         "data": [<list of values aligned with xAxis>]
       }}
     ]
   }}

   If the query does not require a chart, respond with:
   {{ "type": "text", "answer": "<summary>" }}

   Question: {query}
   """


   raw_result = flight_agent.run(prompt)
   print("✅ Agent raw result:", raw_result)
   
   cleaned = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", raw_result, flags=re.DOTALL).strip()
   try:
        return cleaned
   except json.JSONDecodeError as e:
        print("❌ JSON decode failed:", e)
        return {"type": "text", "answer": "Failed to parse chart response."}
