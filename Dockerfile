FROM alpine:latest

WORKDIR /src

RUN apk update && apk add py3-pip python3

COPY app.py /src/app.py
COPY requirements.txt /src/requirements.txt
COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "/src/app.py"]