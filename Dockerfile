FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY multi_tool_agent/ ./multi_tool_agent/

EXPOSE 8001

CMD ["uvicorn", "multi_tool_agent.agent:a2a_app", "--host", "0.0.0.0", "--port", "8001"]
