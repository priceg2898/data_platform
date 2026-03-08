import datetime
import os
from etl.logging_config.log_config import logger
from etl.clients.s3 import s3_conn, s3_put_object


def upload_logs_to_s3(s3_conn, s3_bucket_name, filepath) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        file_content = f.read()

    s3_put_object(
        s3_connection=s3_conn,
        bucket_name=s3_bucket_name,
        bucket_key=f"logs/log_{datetime.datetime.now().isoformat(timespec='seconds')}.jsonl",
        content=file_content,
    )

    return None


if __name__ == "__main__":

    aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    aws_region_name = os.environ["AWS_REGION_NAME"]

    s3 = s3_conn(aws_access_key_id, aws_secret_access_key, aws_region_name)

    file_path = r"/app/logs/log.jsonl"

    try:
        upload_logs_to_s3(
            s3_conn=s3, s3_bucket_name="data-platform-log-storage", filepath=file_path
        )
        logger.info("uploaded logs to s3", stage="log upload")
        os.remove(file_path)
    except ValueError as e:
        logger.exception(f"{e}", stage="s3 upload")
