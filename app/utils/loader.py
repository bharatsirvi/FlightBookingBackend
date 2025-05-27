import pandas as pd

def load_data():
    bookings = pd.read_csv("app/data/flightbooking.csv")
    airlines = pd.read_csv("app/data/airline_id_to_name.csv")
    airline_map = dict(zip(airlines["airlie_id"], airlines["airline_name"]))
    return bookings, airline_map
