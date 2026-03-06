import os
from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.hooks.base import BaseHook
from docker.types import Mount


conn = BaseHook.get_connection("local_postgres")
s3_conn = BaseHook.get_connection("S3")

envVars = {
    "DB_HOST": conn.host,
    "DB_PORT": str(conn.port),
    "DB_NAME": conn.schema,
    "DB_USER": conn.login,
    "DB_PASSWORD": conn.password,
    "AWS_ACCESS_KEY_ID": s3_conn.login,
    "AWS_SECRET_ACCESS_KEY": s3_conn.password,
    "AWS_REGION_NAME": s3_conn.extra_dejson.get("region_name"),
}

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
        command="python -m etl.pipelines.fpl_data_pipeline",
        mount_tmp_dir=False,
        network_mode="fpl_data_platform_default",
        auto_remove="force",
        environment=envVars,
    )

    # dbt run task
    dbt_run = DockerOperator(
        task_id="dbt_run_1",
        image="fpl_data_platform-scripts_container:latest",
        mount_tmp_dir=False,
        command=(
            "dbt run "
            "--project-dir /work_dir/scripts/dbt/fpl "
            "--profiles-dir /work_dir/scripts/dbt"
        ),
        network_mode="fpl_data_platform_default",
        # mounts=[Mount(source=CONTAINER_SCRIPTS_PATH, target="/work_dir", type="bind")],
        environment={"DBT_PROFILES_DIR": "/work_dir/dbt"},
        auto_remove="force",
    )

    extract_load >> dbt_run
