# Initial image to beggin with
FROM python:3.12-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1


RUN apt-get update && apt-get install -y netcat && apt-get clean

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# To run the entrypoint script when the container starts
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


COPY . .


ENTRYPOINT [ "/app/entrypoint.sh" ]
