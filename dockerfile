# FROM python:3-slim

FROM ubuntu:24.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip install uv
COPY . .

RUN uv pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]