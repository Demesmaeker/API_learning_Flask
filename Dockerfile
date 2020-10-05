FROM python:3.8

COPY . /opt/app
WORKDIR /opt/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py"]