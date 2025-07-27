from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS so React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL here
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

@app.post("/book-ticket")
async def book_ticket(booking: TrainBooking):
    # For simplicity, we just echo back the data with a fake ticket ID
    ticket_id = "TICKET12345"
    return {
        "message": "Train ticket booked successfully!",
        "ticket_id": ticket_id,
        "booking_details": booking
    }
