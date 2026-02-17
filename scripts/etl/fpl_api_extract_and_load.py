import requests
import psycopg2 as psy_pg
import datetime
import json

all_endpoints = [   "bootstrap-static/",
                    "events/",
                    #"game_settings/",
                    #"phases/",
                    #"teams/",
                    #"total_players/",
                    "elements/",
                    #"element_types/",
                    "fixtures/",
                    "event-status/",
                    "team/set-piece-notes/"]
                    #"element-summary/{element_id}/",
                    #"event/{event_id}/live/",
                    #"entry/{manager_id}/",
                    #"entry/{manager_id}/history/",
                    #"leagues-classic/{league_id}/standings/",
                    #"entry/{manager_id}/event/{event_id}/picks/"

endpoints = all_endpoints

import psycopg2 as psy_pg
import requests
import json

base_url = "https://fantasy.premierleague.com/api/"

with psy_pg.connect("dbname=test_db user=local_testing password=local_testing_password host=postgres"
) as conn:
    
    with conn.cursor() as cur:
        
        for e in endpoints:
            response = requests.get(f"{base_url}/{e}")

            if response.status_code == 200:
                data = response.json()

                payload = "INSERT INTO bronze.raw_landing (base_url, endpoint, raw_json) VALUES (%s, %s, %s)"

                cur.execute(payload, (base_url, e, json.dumps(data)))
            else:
                print("Error:", f"{base_url} {e} {response.status_code}")
