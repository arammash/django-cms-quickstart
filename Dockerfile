FROM python:3.11

WORKDIR /app

RUN python -m pip install --upgrade pip

# Optimize caching
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .

RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3"]