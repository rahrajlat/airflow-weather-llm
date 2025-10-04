FROM apache/airflow:2.10.3
COPY requirements.txt .
USER root
RUN mkdir -p /tmp;chmod 777 /tmp;
RUN chmod 777 /opt/airflow/logs;
RUN mkdir -p /usr/local/airflow/dags/my_dags/dbt;chmod 777 /usr/local/airflow/dags/my_dags/dbt;
RUN mkdir -p /usr/local/airflow/dags/my_dags/sql;chmod 777 /usr/local/airflow/dags/my_dags/sql;
RUN mkdir -p /usr/local/airflow/tmp;chmod 777 /usr/local/airflow/tmp;
RUN echo "WTF_CSRF_ENABLED= False" > webserver_config.py
USER airflow
RUN pip install --no-cache-dir -r requirements.txt