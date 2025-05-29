# Flight Booking Backend

This is a FastAPI backend for flight booking analytics, using LangChain and LLMs for intelligent data analysis.

---

## 🚀 Features

- FastAPI server with CORS enabled for local frontend development
- LangChain agent for querying flight booking data using natural language
- Data stored in CSV files (`flightbooking.csv`, `airline_id_to_name.csv`)
- Environment variable support via `.env`

---

## 🛠️ Setup Instructions

### 1. **Clone the repository**

```sh
git clone <your-repo-url>
cd flight_booking_backend
```

### 2. **Create and activate a virtual environment (recommended)**

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install dependencies**

```sh
pip install -r requirements.txt
```

### 4. **Set up environment variables**

- Make sure you have a `.env` file in the project root with your OpenRouter API key:

```
OPENROUTER_API_KEY=sk-...
```


## ▶️ Running the Server

```sh
uvicorn main:app --reload
```

- The server will start at [http://127.0.0.1:8000](http://127.0.0.1:8000)
- API endpoints are available under `/api`, e.g. `POST /api/query`

---

## 🧪 Example Query

Send a POST request to `/api/query` with JSON body:

```json
{
  "query": "Show top 5 performing airlines by loyalty points"
}
```

---

## 📁 Project Structure

```
flight_booking_backend/
│
├── main.py
├── requirements.txt
├── .env
└── app/
    ├── api/
    │   └── routes.py
    ├── data/
    │   ├── flightbooking.csv
    │   └── airline_id_to_name.csv
    └── services/
        ├── agent.py
        └── lang_agent.py
```

---

## 📝 Notes

- Make sure your Python version is 3.8 or higher.
- The backend is designed to work with a React frontend (see CORS settings in `main.py`).
- For any issues, check the console output for error messages.

---

**Enjoy your flight booking analytics API!**