import json
from etl.clients.fpl_api import call_api
from etl.clients.postgres import insert_payload
from etl.logging_config.log_config import logger
from etl.clients.s3 import s3_conn, s3_put_object, make_s3_key


all_endpoints = [
    "bootstrap-static/",
    "events/",
    "elements/",
    "fixtures/",
    "event-status/",
    "team/set-piece-notes/",
]

endpoints = all_endpoints

base_url = "https://fantasy.premierleague.com/api"


def run_pipeline(
    conn, endpoints: list[str], base_url: str, s3_conn, s3_bucket_name
) -> None:
    logger.info("pipeline_started...", pipeline="fpl")
    for endpoint in endpoints:
        try:
            data = call_api(base_url, endpoint).json()
            try:
                s3_put_object(
                    s3_connection=s3_conn,
                    bucket_name=s3_bucket_name,
                    bucket_key=f"data/{make_s3_key(base_url,endpoint)}",
                    content=json.dumps(data),
                )
                logger.info(
                    "upload to s3",
                    pipeline="fpl",
                    size=len(json.dumps(data).encode("utf-8")),
                    stage="s3 api output upload",
                    api=base_url,
                    endpoint_name=endpoint,
                )
            except ValueError as e:
                logger.exception(f"{e}", stage="s3 upload")

            try:
                insert_payload(conn, base_url, endpoint, data)
                logger.info(
                    "insert_success",
                    pipeline="fpl",
                    stage="postgresql insert",
                    api=base_url,
                    endpoint_name=endpoint,
                )
            except ValueError as e:
                logger.error(f"{e}")
        except:
            logger.exception(
                "failed to call API",
                pipeline="fpl",
                stage="API call",
                api=base_url,
                endpoint_name=endpoint,
            )


if __name__ == "__main__":
    import psycopg2 as psy_pg
    import os

    conn = psy_pg.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=os.environ.get("DB_PORT", 5432),
    )

    aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    aws_region_name = os.environ["AWS_REGION_NAME"]

    s3 = s3_conn(aws_access_key_id, aws_secret_access_key, aws_region_name)

    try:
        run_pipeline(
            conn, endpoints, base_url, s3, s3_bucket_name="data-platform-log-storage"
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
