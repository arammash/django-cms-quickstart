FROM python:3.11

WORKDIR /app

RUN python -m pip install --upgrade pip

# Optimize caching
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .

# Force Django dev server so we can see the exact error traceback
EXPOSE 10000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:10000"]

