import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from langchain.llms import OpenAI
# Removed import from openai.exceptions to avoid import errors
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from React frontend at localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change this based on your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for flight booking request, with alias for 'from'
class FlightBookingRequest(BaseModel):
    from_: str = Field(..., alias="from")  # 'from' is a reserved keyword in Python
    to: str
    departureDate: str
    returnDate: str = None
    passengers: int

    class Config:
        allow_population_by_field_name = True

def get_openai_api_key():
    # Load API key from environment variable OPENAI_API_KEY (do NOT hardcode your key)
    key = os.getenv("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")
    if not key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
    else:
        print("OpenAI API key loaded successfully.")
    return key

@app.post("/api/flight-book")
async def book_flight(data: FlightBookingRequest, request: Request):
    print(f"Received booking request from {request.client.host}: {data}")

    api_key = get_openai_api_key()
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured.")

    # Construct prompt based on booking data
    prompt = f"Book a flight from {data.from_} to {data.to} departing on {data.departureDate}"
    if data.returnDate:
        prompt += f" returning on {data.returnDate}"
    prompt += f" for {data.passengers} passenger(s)."

    print(f"Constructed prompt for LLM:\n{prompt}")

    try:
        llm = OpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)
        response = llm(prompt)
        print(f"LLM response: {response}")
    except Exception as e:
        # Catch all exceptions including rate limit issues.
        error_message = str(e).lower()
        print(f"OpenAI API call error: {e}")
        if "rate limit" in error_message or "quota" in error_message or "429" in error_message:
            raise HTTPException(status_code=429, detail="OpenAI API quota exceeded or rate limit hit. Please try again later.")
        else:
            raise HTTPException(status_code=500, detail="Error communicating with OpenAI API.") from e

    ticket_confirmation = "Flight booked: confirmation #XYZ123"

    return {
        "agent_reply": response,
        "status": ticket_confirmation,
        "booking_details": data.dict(by_alias=True),
    }
