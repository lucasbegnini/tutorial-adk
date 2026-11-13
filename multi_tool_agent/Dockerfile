# Dockerfile for the weather/time agent (remote A2A server)
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only this agent's package
COPY multi_tool_agent/ ./multi_tool_agent/

# A2A server port
EXPOSE 8001

CMD ["uvicorn", "multi_tool_agent.a2a_server:a2a_app", "--host", "0.0.0.0", "--port", "8001"]
