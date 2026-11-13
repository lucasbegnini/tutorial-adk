# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A2A server entrypoint for the weather/time agent.

Exposes the root_agent via the A2A protocol using the to_a2a() wrapper,
following the ADK A2A Quickstart (Exposing):
https://adk.dev/a2a/quickstart-exposing/

Run it with uvicorn:

    uvicorn multi_tool_agent.a2a_server:a2a_app --host 0.0.0.0 --port 8001
"""

import os

from dotenv import load_dotenv

from google.adk.a2a.utils.agent_to_a2a import to_a2a

from .agent import root_agent

# Load the agent's .env file (e.g. GOOGLE_API_KEY) when running via uvicorn,
# since the adk CLI is not involved here.
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Host and port advertised in the auto-generated agent card.
# Locally this is "localhost"; inside docker-compose it must be the service
# name ("weather-agent") so other containers can reach this server.
A2A_HOST = os.getenv("A2A_HOST", "localhost")
A2A_PORT = int(os.getenv("A2A_PORT", "8001"))

# Make the agent A2A-compatible. The to_a2a() function auto-generates an
# agent card in-memory, served at /.well-known/agent-card.json.
a2a_app = to_a2a(root_agent, host=A2A_HOST, port=A2A_PORT)
