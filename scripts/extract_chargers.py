import os
import requests
import dotenv
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()

URL_LOCATIONS = "https://ocpi.mobinteli.com/2.2/locations"
RELOAD = True


def connect_database():
    # Load secrets
    server = os.environ["MONGO_SERVER"]
    user = os.environ["MONGO_USER"]
    password = os.environ["MONGO_PASSWORD"]

    # Make URI
    uri = "mongodb+srv://{user}:{password}@{server}/?retryWrites=true&w=majority"
    uri = uri.format(
        server=server,
        user=user,
        password=password
    )

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client


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
