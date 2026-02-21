import os
from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

# Path inside the worker container where scripts are mounted
# CONTAINER_SCRIPTS_PATH = "/opt/airflow/scripts"

with DAG(
    dag_id="fpl_api_extract_and_dbt_transform",
    start_date=datetime(2026, 2, 19),
    schedule="@daily",
    catchup=False,
    tags=["dev", "etl"],
) as dag:

    # ETL extract/load task
    extract_load = DockerOperator(
        task_id="etl_extract_load",
        image="fpl_data_platform-scripts_container:latest",
        command="python /work_dir/scripts/etl/fpl_api_extract_and_load.py",
        network_mode="fpl_data_platform_default",
        #mounts=[Mount(source=CONTAINER_SCRIPTS_PATH, target="/work_dir", type="bind")],
        auto_remove="force",
    )

    # dbt run task
    dbt_run = DockerOperator(
        task_id="dbt_run_1",
        image="fpl_data_platform-scripts_container:latest",
        command=(
    "dbt run "
    "--project-dir /work_dir/scripts/dbt/fpl "
    "--profiles-dir /work_dir/scripts/dbt"
),
        network_mode="fpl_data_platform_default",
        #mounts=[Mount(source=CONTAINER_SCRIPTS_PATH, target="/work_dir", type="bind")],
        environment={"DBT_PROFILES_DIR": "/work_dir/dbt"},
        auto_remove="force",
    )

    # Task dependency
    extract_load >> dbt_run