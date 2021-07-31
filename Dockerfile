FROM python:3.8.10-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /yahtzee_backend
COPY . .

## Run tests
#ENV PYTHONPATH="/yahtzee_backend/src/app/:${PYTHONPATH}"
#RUN ["python3", "-m", "unittest", "-v"]

# Start main.py
ENTRYPOINT python3 -u src/app/main.py
