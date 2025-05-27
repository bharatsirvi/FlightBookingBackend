from app.utils.loader import load_data
from datetime import datetime, timedelta

bookings, airline_map = load_data()

def get_airline_name(id):
    return airline_map.get(id, id)

def basic_query_handler(query: str) -> str:
    query = query.lower()

    if "most flights" in query:
        top = bookings["airlie_id"].value_counts().idxmax()
        count = bookings["airlie_id"].value_counts().max()
        return f"{get_airline_name(top)} has the most flights with {count} bookings."

    elif "top three most frequented destinations" in query:
        top3 = bookings["arrival_dt"].value_counts().head(3)
        return ", ".join([f"{k} ({v})" for k, v in top3.items()])

    elif "american airlines yesterday" in query:
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        filtered = bookings[
            (bookings["departure_dt"].str.startswith(yesterday)) &
            (bookings["airlie_id"].map(get_airline_name).str.lower().str.contains("american"))
        ]
        return f"American Airlines had {len(filtered)} bookings on {yesterday}."

    return None
