FROM python:3.11-slim-buster

WORKDIR ./front

RUN apt-get update && apt-get install -y procps && pip install -U pip && rm /etc/localtime && ln -s /usr/share/zoneinfo/America/Mexico_City /

COPY ./requirements.txt front/requirements.txt
RUN pip install -r front/requirements.txt

COPY ./app.py front/app.py

EXPOSE 8501

CMD ["streamlit", "run", "front/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
