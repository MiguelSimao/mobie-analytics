import os
import json
import requests
import pandas as pd
from src.data_collection.db import connect_database

LOCATIONS_URL = "https://pgm.mobie.pt/integration/locations"
LOCATIONS_APIKEY = "id4h40E75o64H4e4uXheqcg1o"
LOCATIONS_USER = "mobie-public-site"
LOCATIONS_PASS = "0cu3NA0^1B$x9KhvJCZmTHv@K"
RELOAD = True


def chargers_etl():

    # Extract data
    os.makedirs("data", exist_ok=True)
    if RELOAD or not os.path.exists(os.path.join("data", "chargers.json")):
        print("Downloading charger data...")
        response = requests.get(
            LOCATIONS_URL, 
            auth=(LOCATIONS_USER, LOCATIONS_PASS),
            headers={"Api-Key": LOCATIONS_APIKEY},
        )
        print("Done. Writing to disk...")
        # Take only location data:
        data = json.dumps(json.loads(response.text)['data'])
        # Write to disk:
        open(os.path.join("data", "chargers.json"), "w").write(data)
        print("Done")

    # Transform with pandas
    df = pd.read_json(os.path.join("data", "chargers.json"))

    # Cleaning
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    
    # Load into Mongo
    client = connect_database()
    result = client["mobie_analytics"]["chargers"].insert_many(df.to_dict("records"))
    print(f"Inserted {len(result.inserted_ids)} docs.")


if __name__ == "__main__":
    chargers_etl()
