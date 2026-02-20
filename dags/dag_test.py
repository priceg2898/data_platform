from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_world():
    print("Hello World!")

with DAG(
    dag_id="my_first_dag",
    start_date=datetime(2026, 2, 19),
    schedule="@daily",
    catchup=False,
) as dag:
    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=hello_world
    )