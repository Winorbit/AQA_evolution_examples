FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /api
WORKDIR /api

RUN apt-get update -y
RUN /usr/local/bin/python -m pip install --upgrade pip 

RUN pip install -r requirements.txt

CMD ["python", "run.py"]