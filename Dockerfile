FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ARG CACHEBUST=1

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "ecommerce_api.wsgi:application", "--bind", "0.0.0.0:8000"]
