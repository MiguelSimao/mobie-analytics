import os
from datetime import datetime
import requests
import dotenv
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()

URL_TARIFFS = "https://www.mobie.pt/documents/42032/106470/Tarifas"
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


def tariffs_etl():

    # Extract data
    os.makedirs("data", exist_ok=True)
    if RELOAD or not os.path.exists(os.path.join("data", "tariffs.csv")):
        print("Downloading tariff data...")
        response = requests.get(URL_TARIFFS)
        open(os.path.join("data", "tariffs.csv"), "w").write(response.text)
        open(os.path.join("data", "tariffs_dt"), "w").write(datetime.utcnow().isoformat())

    # Transform with pandas
    print("Transforming tariff data...")
    df = pd.read_csv(os.path.join("data", "tariffs.csv"), sep=";")
    dt = open(os.path.join("data", "tariffs_dt"), "r").read()

    # Cleaning
    df = df.rename(columns={"ChargingStation": "id"})
    docs = []
    for station, station_data in df.groupby('id'):
        docs.append(
            {
                "id": station,
                "last_updated": dt,
                "tariff": station_data.drop(columns=['id']).to_dict('records'),
            }
        )
        
    # Load into Mongo
    print("Pushing tariff data...")
    client = connect_database()
    result = client["mobie_analytics"]["tariffs"].insert_many(docs)
    print(f"Inserted {len(result.inserted_ids)} docs.")


if __name__ == "__main__":
    tariffs_etl()