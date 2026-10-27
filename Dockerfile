FROM python:3.11

WORKDIR /app

RUN python -m pip install --upgrade pip

# Optimize caching
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .

# Force migrations to run right before uWSGI boots up
CMD ["sh", "-c", "python manage.py migrate --noinput && uwsgi --ini wsgi.ini"]