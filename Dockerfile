FROM python:3.8-alpine

RUN apk update

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ /app/api/

EXPOSE 5000
CMD [ "python", "api/api.py" ]