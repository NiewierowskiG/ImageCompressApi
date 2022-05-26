FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /Django_gn
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt