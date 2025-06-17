# agents/appointment_agent.py
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from services.calendar_service import create_appointment

def build_appointment_agent():
    llm = ChatOpenAI()
    tools = [
        Tool(name="Schedule Appointment", func=create_appointment, description="Schedule an appointment on calendar")
    ]
    return initialize_agent(tools, llm, agent="chat-zero-shot-react-description", verbose=True)
