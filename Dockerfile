FROM python:3.8.10-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /yahtzee_backend/src/app
COPY . .
ENTRYPOINT python3 -u src/app/main.py
