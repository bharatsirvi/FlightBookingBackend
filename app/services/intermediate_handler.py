from app.utils.loader import load_data
import pandas as pd

bookings, airline_map = load_data()

def get_airline_name(id):
    return airline_map.get(id, id)

def intermediate_query_handler(query: str):
    query = query.lower()
  
    if "average flight delay per airline" in query:
        bookings["departure_dt"] = pd.to_datetime(bookings["departure_dt"] + ' ' + bookings["dep_time"])
        bookings["arrival_dt"] = pd.to_datetime(bookings["arrival_dt"] + ' ' + bookings["arrivl_time"])

        bookings["delay"] = (bookings["arrival_dt"] - bookings["departure_dt"]).dt.total_seconds() / 60
        avg_delay = bookings.groupby("airlie_id")["delay"].mean().sort_values(ascending=False)

        return {
            "type": "bar",
            "description": "Average flight delay per airline (in minutes)",
            "data": [{"airline": get_airline_name(k), "delay": round(v, 2)} for k, v in avg_delay.items()],
            "meta": {"x": "airline", "y": "delay"}
        }

    elif "month with the highest number of bookings" in query:
        bookings["month"] = pd.to_datetime(bookings["departure_dt"]).dt.month_name()
        top_month = bookings["month"].value_counts().idxmax()
        count = bookings["month"].value_counts().max()

        return {
            "type": "text",
            "description": f"{top_month} had the highest number of bookings ({count})"
        }

    return None
