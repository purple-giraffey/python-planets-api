FROM python:3.8
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "main:app", "--host=0.0.0.0"]