FROM python:slim

WORKDIR /mongodb

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app .
COPY data .
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]