FROM python:3.11-slim-buster

WORKDIR /.

RUN apt-get update && apt-get install -y procps && pip install -U pip && rm /etc/localtime && ln -s /usr/share/zoneinfo/America/Mexico_City /

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./main.py ./main.py

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
