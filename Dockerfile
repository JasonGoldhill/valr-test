FROM python:3.8-alpine

RUN apk update

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY api/api.py /app/api/
COPY api/orderbook.py /app/api/

EXPOSE 5000
CMD [ "python", "api/api.py" ]