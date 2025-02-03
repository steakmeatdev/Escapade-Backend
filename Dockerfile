FROM python:3.12-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Install netcat (used for waiting for the database to be ready)
RUN apt-get update && apt-get install -y netcat && apt-get clean

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy entrypoint.sh, fix line endings, and make it executable
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy the rest of the app
COPY . .

# Set entrypoint to entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]
