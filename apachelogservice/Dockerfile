FROM python:3.8.5
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /apachelogservice
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn apachelogservice.wsgi:application --bind 0.0.0.0:8000
