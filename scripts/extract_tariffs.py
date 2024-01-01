import os
import json
from datetime import datetime
import requests
import dotenv
import pandas as pd
import tqdm
from src.data_collection.db import connect_database

dotenv.load_dotenv()

LOCATIONS_URL = "https://pgm.mobie.pt/integration/locations"
LOCATIONS_APIKEY = "id4h40E75o64H4e4uXheqcg1o"
LOCATIONS_USER = "mobie-public-site"
LOCATIONS_PASS = "0cu3NA0^1B$x9KhvJCZmTHv@K"
RELOAD = True


def tariffs_etl():

    # Step 1: Extract locations

    print("Downloading charger data...")
    response = requests.get(
        LOCATIONS_URL, 
        auth=(LOCATIONS_USER, LOCATIONS_PASS),
        headers={"Api-Key": LOCATIONS_APIKEY},
    )
    locations = json.loads(response.text)["data"]

    # Step 2: Iterate over locations to extract tariffs
    tariffs = []
    for location in tqdm.tqdm(locations):
        charger_id = location["id"]
        response = requests.get(
            f"{LOCATIONS_URL}/{charger_id}", 
            auth=(LOCATIONS_USER, LOCATIONS_PASS),
            headers={"Api-Key": LOCATIONS_APIKEY},
        )
        data = json.loads(response.text)['data']
        data = {
            "_format": "202311",
            **data
        }
        tariffs.append(data)

    # Store locally
    os.makedirs("data", exist_ok=True)
    with open(os.path.join("data", "tariffs.json"), "w") as fp:
        json.dump(tariffs, fp)

    # Load into Mongo
    print("Pushing tariff data...")
    client = connect_database()
    result = client["mobie_analytics"]["tariffs"].insert_many(tariffs)
    print(f"Inserted {len(result.inserted_ids)} docs.")


if __name__ == "__main__":
    tariffs_etl()
