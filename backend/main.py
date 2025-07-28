from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow CORS so React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrainBooking(BaseModel):
    name: str
    age: int
    source: str
    destination: str
    date: str  # YYYY-MM-DD
    train_number: str

# Replace these with your actual RapidAPI details
RAPIDAPI_KEY = "cfa2cbd9a1msh21ffb63abfd755ep13556cjsn224a213cf46f"
RAPIDAPI_HOST = "irctc1.p.rapidapi.com"  # e.g., "indianrailways.p.rapidapi.com"

@app.post("/book-ticket")
async def book_ticket(booking: TrainBooking):
    # Example: Call external API to fetch train info before booking
    url = f"https://{RAPIDAPI_HOST}/trainInfo"  # Adjust endpoint accordingly
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }
    params = {"trainno": booking.train_number}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        # Return a HTTP 502 Bad Gateway error if external API fails
        raise HTTPException(status_code=502, detail=f"Failed to fetch train info: {e}")

    train_info = response.json()

    # You can add more validation logic here, for example:
    # - Confirm train exists
    # - Check source/destination in train_info
    # - Validate travel date based on train schedule

    # For demonstration, generate a fake ticket id
    ticket_id = "TICKET12345"

    return {
        "message": "Train ticket booked successfully!",
        "ticket_id": ticket_id,
        "train_info": train_info,
        "booking_details": booking,
    }
