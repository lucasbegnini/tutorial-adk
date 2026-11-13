
import os

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Base URL of the remote weather/time A2A server.
# Locally it runs on localhost:8001; inside docker-compose it is reachable
# through the "weather-agent" service name (set via WEATHER_AGENT_URL).
WEATHER_AGENT_URL = os.getenv("WEATHER_AGENT_URL", "http://localhost:8001")


def greet(name: str) -> dict:
    """Greets the user by name.

    Args:
        name (str): The name of the person to greet.

    Returns:
        dict: status and result or error msg.
    """
    if name:
        return {
            "status": "success",
            "report": f"Hello, {name}! Nice to meet you. How can I help you today?",
        }
    else:
        return {
            "status": "error",
            "error_message": "No name was provided for the greeting.",
        }


def say_goodbye(name: str) -> dict:
    """Says goodbye to the user by name.

    Args:
        name (str): The name of the person to say goodbye to.

    Returns:
        dict: status and result or error msg.
    """
    if name:
        return {
            "status": "success",
            "report": f"Goodbye, {name}! Have a great day. See you soon!",
        }
    else:
        return {
            "status": "error",
            "error_message": "No name was provided for the farewell.",
        }


# Remote A2A agent: the weather/time agent exposed by multi_tool_agent.
# The agent card is fetched from the well-known path of the remote server.
weather_time_agent = RemoteA2aAgent(
    name="weather_time_agent",
    description=(
        "Remote agent that answers questions about the time and weather "
        "in a city."
    ),
    agent_card=(
        f"{WEATHER_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)


root_agent = Agent(
    name="orchestrator",
    model="gemini-flash-latest",
    description=(
        "Agent that greets users, says goodbye, and delegates weather and "
        "time questions to a remote agent via A2A."
    ),
    instruction=(
        "You are a friendly orchestrator agent. "
        "When a user starts a conversation or asks to be greeted, use the 'greet' tool with their name. "
        "When a user leaves, ends the conversation, or asks to say goodbye, use the 'say_goodbye' tool with their name. "
        "When a user asks about the weather or the current time in a city, delegate the request to the 'weather_time_agent' sub-agent. "
        "If you don't know the user's name, ask for it politely before calling the greeting tools."
    ),
    tools=[greet, say_goodbye],
    sub_agents=[weather_time_agent],
)
