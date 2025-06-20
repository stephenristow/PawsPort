
# Use official Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system deps (including MySQL client!)
RUN apt-get update && apt-get install -y \
    netcat-openbsd gcc \
    default-libmysqlclient-dev \
    libmysqlclient-dev \
    mysql-client \
    pkg-config \
    python3-dev

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and schema.sql
COPY . .
COPY schema.sql /app/schema.sql

# Collect static files (if any)
RUN python manage.py collectstatic --noinput || true

# Expose the Django port
EXPOSE 8000

# Entrypoint command: run server AND initialize schema if necessary
CMD sh -c "
    sleep 5 && \
    mysql -h \"$DB_HOST\" -u \"$DB_USER\" -p\"$DB_PASSWORD\" \"$DB_NAME\" < /Users/stephenristow/Projects/PawsPort/db-init/init-db.sql || true && \
    python manage.py runserver 0.0.0.0:8000
"


