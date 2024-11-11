# syntax=docker/dockerfile:1

FROM python:3.13
WORKDIR /
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 50505
ENTRYPOINT ["gunicorn", "app:app"]