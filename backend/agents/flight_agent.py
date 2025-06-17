# agents/flight_agent.py
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from services.flight_api_service import search_flights, book_flight

def build_flight_agent():
    llm = ChatOpenAI()
    tools = [
        Tool(name="Search Flights", func=search_flights, description="Search available flights"),
        Tool(name="Book Flight", func=book_flight, description="Book a flight with passenger details")
    ]
    return initialize_agent(tools, llm, agent="chat-zero-shot-react-description", verbose=True)
