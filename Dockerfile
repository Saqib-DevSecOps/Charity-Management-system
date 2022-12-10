FROM python:3.8.0
USER root
WORKDIR /charity
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000 
