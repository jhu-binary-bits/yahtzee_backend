FROM python:3.8.10-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /yahtzee_backend
COPY . .
ENTRYPOINT python3 src/app/main.py