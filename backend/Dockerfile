FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN [ "pip", "install", "-r", "requirements.txt" ]

COPY api /app/api/

# CMD [ "fastapi", "run", "--reload","api/main.py" ]
CMD ["uvicorn", "api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]