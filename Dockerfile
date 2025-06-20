
# Use official Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
	netcat-openbsd gcc \
	gcc \
	default-libmysqlclient-dev \
	libmariadb-dev \
	mariadb-client \
	pkg-config \
	python3-dev

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .
COPY db-init/init-db.sql /app/init-db.sql

# Run collectstatic if using static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

#CMD ["sh", "-c", "python manage.py migrate && mysql -h \"$MYSQLHOST\" -u \"$MYSQLUSER\" -p\"$MYSQL_PASSWORD\" \"$MYSQL_DATABASE\" < /app/init-db.sql && python manage.py runserver 0.0.0.0:8000"]
CMD ["sh", "-c", "echo HOST=$MYSQLHOST USER=$MYSQLUSER DB=$MYSQL_DATABASE && python manage.py migrate && mysql --protocol=TCP -h \"$MYSQLHOST\" -u \"$MYSQLUSER\" -p\"$MYSQL_PASSWORD\" \"$MYSQL_DATABASE\" < /app/init-db.sql && python manage.py runserver 0.0.0.0:8000"]

