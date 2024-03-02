FROM apache/airflow:2.8.1

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt .

USER airflow

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt  # No need for --user flag here

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID
#docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler
