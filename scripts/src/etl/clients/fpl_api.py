import requests
from etl.logging_config.log_config import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    # before_sleep=before_sleep_log(logger, level="WARNING"),
    reraise=True,
)
def call_api(base_url: str, endpoint: str) -> dict:
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    response = requests.get(url, timeout=10)

    # Explicit retry control for 429 + 5xx
    if response.status_code in {429, 500, 502, 503, 504}:
        logger.warning(f"Retryable error {response.status_code} for {url}")
        response.raise_for_status()

    response.raise_for_status()
    return response
