FROM python:3.11

WORKDIR /app

RUN python -m pip install --upgrade pip

# Optimize caching behavior
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .

# Copy entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Starts uWSGI via the entrypoint script
CMD ["uwsgi", "--ini", "wsgi.ini"]