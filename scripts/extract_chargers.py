import os
import requests
import pandas as pd
from src.data_collection.db import connect_database

URL_LOCATIONS = "https://ocpi.mobinteli.com/2.2/locations"
RELOAD = True


def chargers_etl():

    # Extract data
    os.makedirs("data", exist_ok=True)
    if RELOAD or not os.path.exists(os.path.join("data", "chargers.json")):
        print("Downloading charger data...")
        response = requests.get(URL_LOCATIONS)
        open(os.path.join("data", "chargers.json"), "w").write(response.text)

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
