from psycopg2.extras import Json


def insert_payload(conn, base_url: str, endpoint: str, raw_json: str) -> None:
    payload = """
        INSERT INTO public.fpl_api__raw_landing
        (base_url, endpoint, raw_json)
        VALUES (%s, %s, %s)
    """

    with conn.cursor() as cur:
        cur.execute(payload, (base_url, endpoint, Json(raw_json)))
