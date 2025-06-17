# api/routes/flight_agent.py
from fastapi import APIRouter
from agents.flight_agent import build_flight_agent

router = APIRouter()

@router.post("/search")
def search_flight(prompt: str):
    return build_flight_agent().run(prompt)

@router.post("/book")
def book_flight(prompt: str):
    return build_flight_agent().run(prompt)
