FROM python:3.9-slim-bookworm

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt && pip cache purge

CMD ["python3", "main.py"]
