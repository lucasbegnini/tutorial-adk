# ADK Tutorial — Agents with A2A

Study project for the [Agent Development Kit (ADK)](https://adk.dev/) featuring two agents communicating via the **A2A (Agent2Agent) protocol**, following the official quickstarts:

- [Multi-Tool Agent](https://adk.dev/tutorials/multi-tool-agent/)
- [A2A Quickstart (Consuming)](https://adk.dev/a2a/quickstart-consuming/)
- [A2A Quickstart (Exposing)](https://adk.dev/a2a/quickstart-exposing/)


## Architecture

```
┌─────────────────────┐         A2A Protocol         ┌──────────────────────┐
│    orchestrator     │ ───────────────────────────▶ │   multi_tool_agent   │
│  (adk web, :8000)   │   delegates weather & time   │  (A2A server, :8001) │
│                     │   questions via RemoteA2aAgent│  (weather + time)   │
└─────────────────────┘                              └──────────────────────┘
```

- **`orchestrator`** — greetings agent (`greet` / `say_goodbye`) that also **consumes** the remote agent via A2A using `RemoteA2aAgent`. This is the agent the user talks to (web UI or API).
- **`multi_tool_agent`** — weather and time agent (`get_weather` / `get_current_time`), **exposed** via A2A with `to_a2a()` + `uvicorn`. The agent card is automatically generated at `/.well-known/agent-card.json`.

## Project structure

```
tutorial-adk/
├── multi_tool_agent/        # Remote agent (weather/time)
│   ├── agent.py             # Agent definition and tools
│   ├── a2a_server.py        # A2A entrypoint (to_a2a + uvicorn)
│   ├── __init__.py
│   ├── .env                 # GOOGLE_API_KEY
│   └── Dockerfile           # A2A server image
├── orchestrator/            # Consuming agent (greetings + A2A)
│   ├── agent.py             # RemoteA2aAgent + greeting tools
│   ├── __init__.py
│   ├── .env                 # GOOGLE_API_KEY
│   └── Dockerfile           # adk web image
├── docker-compose.yml
├── requirements.txt
└── .dockerignore
```

## Prerequisites

- Python 3.13+ (or Docker)
- A `GOOGLE_API_KEY` set in each agent's `.env` file:

```bash
GOOGLE_API_KEY="your-key-here"
```

This project uses Gemini by default. If you want to plug in and use other LLMs, see the documentation here: https://adk.dev/agents/models/

## Running locally (without Docker)

Install the dependencies (preferably in a venv):

```bash
pip install -r requirements.txt
```

**Terminal 1** — start the weather/time A2A server (port 8001):

```bash
uvicorn multi_tool_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8001
```

Check the auto-generated agent card: http://localhost:8001/.well-known/agent-card.json

**Terminal 2** — start the web UI (port 8000):

```bash
adk web
```

Open http://localhost:8000 and select the **orchestrator** agent.

## Running with Docker

Start the full stack (two containers, one per agent):

```bash
docker compose up --build
```

- Orchestrator web UI: http://localhost:8000
- Weather agent card: http://localhost:8001/.well-known/agent-card.json

To stop:

```bash
docker compose down
```

### How the communication works in Docker

- The `weather-agent` advertises the host `weather-agent` (the compose service name) in its agent card, via the `A2A_HOST` / `A2A_PORT` env vars.
- The `orchestrator` receives `WEATHER_AGENT_URL=http://weather-agent:8001` and builds the `AgentCard` in code pointing to that host.
  - The card is built in code (instead of being fetched from the well-known URL) because ADK only accepts card URLs over HTTPS or HTTP on a loopback host — which would not work between containers over plain HTTP.

## Sending messages via curl

The `adk web` API exposes REST endpoints. The flow is: **create the session → send the message**.

### 1. Create the session

The `user_id` and `session_id` go in the URL path:

```bash
curl -X POST "http://localhost:8000/apps/orchestrator/users/lucas/sessions/session-123" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 2. Send the message

Reference the same `user_id` and `session_id` in the body:

```bash
curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "orchestrator",
    "user_id": "lucas",
    "session_id": "session-123",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Hi, my name is Lucas. What is the weather in New York?"}]
    }
  }'
```

Response (a list of ADK events — the orchestrator uses the local `greet` tool and delegates the weather question via A2A):

```
[orchestrator]: Hello Lucas! Nice to meet you.

The current weather in New York is sunny with a temperature of 25°C (77°F).
```

### Tips

- **Reuse the same `session_id`** to keep the conversation context (the agent remembers, for example, your name).
- **Change the `user_id`** to have isolated sessions per user.
- Use the **`/run_sse`** endpoint instead of `/run` if you want a streaming response (Server-Sent Events).
- The `/run` response is a list of **events** (texts, tool calls, transfers between agents). Example filtering only the text parts:

```bash
curl -s -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{"app_name":"orchestrator","user_id":"lucas","session_id":"session-123","new_message":{"role":"user","parts":[{"text":"What time is it in New York?"}]}}' \
  | python3 -c "
import json, sys
for e in json.load(sys.stdin):
    for part in (e.get('content') or {}).get('parts', []):
        if 'text' in part:
            print(f\"[{e.get('author')}]:\", part['text'])
"
```

## Example interactions

| Message | What happens |
|---|---|
| `Hi, my name is Lucas` | Local `greet` tool |
| `Bye!` | Local `say_goodbye` tool |
| `What is the weather in New York?` | Delegated via **A2A** to the `weather_time_agent` |
| `What time is it in New York?` | Delegated via **A2A** to the `weather_time_agent` |

## Environment variables

| Variable | Where | Description | Default |
|---|---|---|---|
| `GOOGLE_API_KEY` | each agent's `.env` | Gemini API key | — |
| `WEATHER_AGENT_URL` | orchestrator | Base URL of the remote A2A server | `http://localhost:8001` |
| `A2A_HOST` | multi_tool_agent | Host advertised in the agent card | `localhost` |
| `A2A_PORT` | multi_tool_agent | Port advertised in the agent card | `8001` |
