from loguru import logger
import traceback
import os
import sys
import uuid
import json

RUN_ID = str(uuid.uuid4())
os.makedirs("/app/logs", exist_ok=True)
logger.remove()


def json_sink(message):
    record = message.record
    exc = record["exception"]
    unhandled = record["extra"].get("unhandled", False)

    exception_text = None
    if exc and unhandled:
        exception_text = "".join(traceback.format_exception(*exc))

    simple_record = {
        "level": record["level"].name,
        "time": record["time"].isoformat(timespec="seconds"),
        "pipeline": record["extra"].get("pipeline"),
        "run_id": record["extra"].get("run_id"),
        "stage": record["extra"].get("stage"),
        "message": record["message"],
        "records": record["extra"].get("records"),
        "size": record["extra"].get("size"),
        "api": record["extra"].get("api"),
        "endpoint_name": record["extra"].get("endpoint_name"),
        "exception": exception_text,
    }

    with open("/app/logs/log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(simple_record) + "\n")

    # Also print to stdout
    print(json.dumps(simple_record), flush=True)


logger.add(json_sink, enqueue=True)

logger = logger.bind(run_id=RUN_ID)


def handle_exception(exc_type, exc_value, exc_traceback):
    logger.bind(unhandled=True).opt(
        exception=(exc_type, exc_value, exc_traceback)
    ).critical("uncaught_exception")


sys.excepthook = handle_exception


"""
# https://www.dash0.com/guides/python-logging-with-loguru

from loguru import logger
import traceback
import os
import sys
import uuid
import json

RUN_ID = str(uuid.uuid4())

os.makedirs("/app/logs", exist_ok=True)

logger.remove()

def json_sink(message):
    record = message.record
    exc = record["exception"]
    unhandled = record["extra"].get("unhandled", False)

    exception_text = None
    if exc and unhandled:
        import traceback
        exception_text = "".join(traceback.format_exception(*exc))

    simple_record = {
        "level": record["level"].name,
        "time": record["time"].isoformat(timespec="seconds"),
        "pipeline": record["extra"].get("pipeline"),
        "run_id": record["extra"].get("run_id"),
        "stage": record["extra"].get("stage"),
        "message": record["message"],
        "records": record["extra"].get("records"),
        "size": record["extra"].get("size"),
        "api": record["extra"].get("api"),
        "endpoint_name": record["extra"].get("endpoint_name"),
        "exception": exception_text,
    }

    with open("/app/logs/pipeline_current.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(simple_record) + "\n")

    print(json.dumps(simple_record), flush=True)

logger.add(json_sink, enqueue=True)

logger = logger.bind(
    run_id=RUN_ID
)

def handle_exception(exc_type, exc_value, exc_traceback):
    logger.bind(unhandled=True).opt(
        exception=(exc_type, exc_value, exc_traceback)
    ).critical("uncaught_exception")

sys.excepthook = handle_exception """
