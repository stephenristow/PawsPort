# Use official Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
	netcat-openbsd gcc \
	gcc \
	default-libmysqlclient-dev \
	pkg-config \
	python3-dev

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run collectstatic if using static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Entry point
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

