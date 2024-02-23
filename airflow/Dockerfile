FROM apache/airflow:latest
USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

USER airflow

# Install provider packages from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uIjoidWtva29iaWxpLmphY29iLmdtYWlsLmNvbSIsImVtYWlsIjoidWtva29iaWxpLmphY29iQGdtYWlsLmNvbSIsInVzZXJJZCI6ImU2OTAwYWJjLWVjNDYtNGUxOS05ZWI2LTE1Y2Y4NjlmYzkzYSIsImlhdCI6MTcwODU0Mjk0MywiZXhwIjoxNzQwMTAwNTQzfQ.CoPLpaxLkHjkkYlWMs_wuSX6TZA3CAVr_7_MkbdIkjA