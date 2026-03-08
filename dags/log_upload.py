import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.hooks.base import BaseHook

conn = BaseHook.get_connection("S3")

env_vars = {
    "AWS_ACCESS_KEY_ID": conn.login,
    "AWS_SECRET_ACCESS_KEY": conn.password,
    "AWS_REGION_NAME": conn.extra_dejson.get("region_name"),
}

with DAG(
    dag_id="log_upload",
    start_date=datetime.datetime(2026, 2, 19),
    schedule="@daily",
    catchup=False,
    tags=["dev", "etl"],
) as dag:

    # ETL extract/load task
    do_upload = DockerOperator(
        task_id="upload_logs_to_s3",
        image="fpl_data_platform-scripts_container:latest",
        command="python -m etl.logging_config.upload_logs_to_s3",
        mount_tmp_dir=False,
        network_mode="fpl_data_platform_default",
        auto_remove="force",
        environment=env_vars,
    )

    do_upload
