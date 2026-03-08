import boto3
import re
import datetime as dt


def s3_conn(access_key: str, secret_key: str, region: str):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )
    return s3


def s3_put_object(s3_connection, bucket_name, bucket_key, content):
    s3_connection.put_object(
        Bucket=bucket_name,
        Key=bucket_key,
        Body=content,
    )
    return None


def make_s3_key(base_url, endpoint):
    timestamp = dt.datetime.now().strftime(
        "%Y-%m-%dT%H-%M-%S"
    )  # ISO-like, safe characters

    safe_url = re.sub(r"[^0-9a-zA-Z]+", "_", base_url.strip("/"))
    safe_endpoint = re.sub(r"[^0-9a-zA-Z]+", "_", endpoint.strip("/"))

    key = f"{timestamp}__{safe_url}__{safe_endpoint}.json"
    return key
