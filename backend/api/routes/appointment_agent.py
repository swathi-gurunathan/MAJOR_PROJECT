# api/routes/appointment_agent.py
from fastapi import APIRouter
from backend.agents.appointment_agent import build_appointment_agent

router = APIRouter()

@router.post("/schedule")
def schedule_appointment(prompt: str):
    return build_appointment_agent().run(prompt)
