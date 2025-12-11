# Lekka baza z Pythonem
FROM python:3.12-slim

# Ustawienia środowiska
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Katalog aplikacji
WORKDIR /app

# Zależności systemowe (jeśli kiedyś będzie potrzebny gcc itp., tu można dodać)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Najpierw requirements, żeby cache lepiej działał
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Potem reszta kodu
COPY . /app

# Zmienna środowiskowa na produkcję (jak będziesz chciał)
ENV FLASK_ENV=production

# Gunicorn będzie słuchał na porcie 8000 w kontenerze
EXPOSE 8000

# Komenda startowa:
# main:app -> moduł main.py i obiekt "app"
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]
