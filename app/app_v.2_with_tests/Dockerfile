FROM python:3.9

COPY . /app
WORKDIR /app

RUN apt-get update -y
RUN /usr/local/bin/python -m pip install --upgrade pip 
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "api/run.py"]