from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from docker.types import Mount


with DAG(
    dag_id="my_first_dag",
    start_date=datetime(2026, 2, 19),
    schedule="@daily",
    catchup=False,
) as dag:

    extract_load = DockerOperator(
        task_id="etl_extract_load",
        image="fpl_data_platform-scripts_container:latest",
        command="python3 etl/fpl_api_extract_and_load.py",
        network_mode="fpl_data_platform_default",
        mounts=[Mount(source="/absolute/path/to/your/project/scripts", target="/work_dir", type="bind")],
        auto_remove="force",
    )

    dbt_run = DockerOperator(
        task_id="dbt_run_1",
        image="fpl_data_platform-scripts_container:latest",
        command="dbt run",
        network_mode="fpl_data_platform_default",
        mounts=[Mount(source="/opt/airflow/scripts", target="/work_dir/dbt/fpl", type="bind")],
        auto_remove="force",
    )


extract_load >> dbt_run