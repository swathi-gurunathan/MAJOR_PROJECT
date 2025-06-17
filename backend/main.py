from fastapi import FastAPI
from .api.routes import flight_agent, appointment_agent
from backend.scheduler.job_scheduler import start_scheduler

app = FastAPI()

app.include_router(flight_agent.router, prefix="/flight")
app.include_router(appointment_agent.router, prefix="/appointment")

start_scheduler()
