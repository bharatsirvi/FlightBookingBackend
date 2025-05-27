from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_community.chat_models import ChatOpenAI
from app.utils.parse_json import parse_json_string
import pandas as pd
import os
from dotenv import load_dotenv

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

    return create_pandas_dataframe_agent(llm, merged_df, verbose=True, allow_dangerous_code=True,handle_parsing_errors=True,)

# Create agent
flight_agent = create_flight_agent()

# Handle queries
def ask_flight_agent(query: str) -> dict:
   print("🧠 Agent received query:", query)
    

   formatted_query = query,

   raw_result = flight_agent.run(formatted_query)
   print("✅ Agent raw result:", raw_result)
   return raw_result if raw_result else None
