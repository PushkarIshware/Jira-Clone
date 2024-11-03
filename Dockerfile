FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

# aub_jira
COPY . .

WORKDIR /app/aub_jira

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]