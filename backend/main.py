from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Define request schema
class BookingRequest(BaseModel):
    name: str
    age: int
    source: str
    destination: str
    date: str  # Format: YYYY-MM-DD
    train_number: str

# Function to call IRCTC RapidAPI
def get_train_schedule(train_number: str):
    url = f"https://irctc1.p.rapidapi.com/api/v1/getTrainSchedule?trainNo={train_number}"

    headers = {
        "X-RapidAPI-Key": "ef226ee913msh80a6ccaa5adf751p1f8f18jsnac962bce22f5",  # Your API key
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch train info: {response.status_code} {response.reason}")

# Endpoint to book ticket
@app.post("/book-ticket")
def book_ticket(booking: BookingRequest):
    try:
        schedule = get_train_schedule(booking.train_number)

        return {
            "message": "Ticket booked successfully!",
            "passenger": {
                "name": booking.name,
                "age": booking.age
            },
            "journey": {
                "from": booking.source,
                "to": booking.destination,
                "date": booking.date,
                "train_number": booking.train_number,
                "train_name": schedule.get("data", {}).get("train_name", "N/A"),
                "route": schedule.get("data", {}).get("route", [])
            }
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

