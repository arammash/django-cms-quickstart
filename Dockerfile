FROM python:3.11

WORKDIR /app

RUN python -m pip install --upgrade pip

# optimizing the docker caching behaviour
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .

# RUN python manage.py collectstatic --noinput

# Run migrations on startup, then start uWSGI
CMD ["sh", "-c", "python manage.py migrate && uwsgi --ini wsgi.ini"]