
from google.adk.agents import Agent


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


root_agent = Agent(
    name="orchestrator",
    model="gemini-flash-latest",
    description=(
        "Agent that greets users and says goodbye to them."
    ),
    instruction=(
        "You are a friendly greeting agent. "
        "When a user starts a conversation or asks to be greeted, use the 'greet' tool with their name. "
        "When a user leaves, ends the conversation, or asks to say goodbye, use the 'say_goodbye' tool with their name. "
        "If you don't know the user's name, ask for it politely before calling the tools."
    ),
    tools=[greet, say_goodbye],
)
