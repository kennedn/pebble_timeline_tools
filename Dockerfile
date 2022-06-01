FROM python:3
WORKDIR /usr/src/app

COPY requirements.txt ./
ENV PYTHONBUFFERED=1
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
