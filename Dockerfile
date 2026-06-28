FROM python:3.13.14-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /restroApp

WORKDIR /restroApp

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /restroApp/

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]