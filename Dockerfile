FROM python:3.5-alpine

MAINTAINER Maksim Ryndin "maksim.ryndin@gmail.com"

RUN apk add --no-cache gcc musl-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]

EXPOSE 8888
