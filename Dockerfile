FROM python:3.11-alpine
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD . /files
WORKDIR /files

ENTRYPOINT ["behave"]