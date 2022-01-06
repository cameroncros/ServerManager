FROM python:3-alpine
RUN apk update && apk add openssh
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN mkdir /app
COPY main.py /app
EXPOSE 7475
WORKDIR /app
CMD python main.py
