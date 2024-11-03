FROM python:3.11

RUN mkdir /yandexflat

WORKDIR /yandexflat

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head && gunicorn src.main:app -w 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000"]
