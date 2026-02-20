import os
from docker.types import Mount
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

HOST_ETL = os.path.abspath("./scripts")
HOST_DBT = os.path.abspath("./scripts/dbt/fpl")

with DAG(
    dag_id="my_first_dag",
    start_date=datetime(2026, 2, 19),
    schedule="@daily",
    catchup=False,
) as dag:

    extract_load = DockerOperator(
        task_id="etl_extract_load",
        image="fpl_data_platform-scripts_container:latest",
        command="python /work_dir/etl/fpl_api_extract_and_load.py",
        network_mode="fpl_data_platform_default",
        mounts=[Mount(source=HOST_ETL, target="/work_dir/etl", type="bind")],
        auto_remove="force",
    )

    dbt_run = DockerOperator(
        task_id="dbt_run_1",
        image="fpl_data_platform-scripts_container:latest",
        command="dbt run --project-dir /work_dir/dbt",
        network_mode="fpl_data_platform_default",
        mounts=[Mount(source=HOST_DBT, target="/work_dir/dbt", type="bind")],
        auto_remove="force",
    )

    extract_load >> dbt_run