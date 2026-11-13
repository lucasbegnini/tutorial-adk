# Dockerfile for the orchestrator agent (consuming agent with web UI)
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only this agent's package (the weather/time agent is consumed
# remotely via A2A, so it is not needed in this image)
COPY orchestrator/ ./orchestrator/

# adk web port
EXPOSE 8000

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000", "/app"]
