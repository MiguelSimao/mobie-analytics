import os
from io import BytesIO
import requests
import pandas as pd


RELOAD = True
GSHEETS_PAGES_URLS = [
    # (target name, header index, url)
    ("ceme_plans", 3, "https://docs.google.com/spreadsheets/d/1c1itP5vir1xZ9BkfJGehJyoEro6UhncgRw-fLw5m6MQ/export?format=csv&id=1c1itP5vir1xZ9BkfJGehJyoEro6UhncgRw-fLw5m6MQ&gid=1552482801"),
    ("erse_tar", 3, "https://docs.google.com/spreadsheets/d/1c1itP5vir1xZ9BkfJGehJyoEro6UhncgRw-fLw5m6MQ/export?format=csv&id=1c1itP5vir1xZ9BkfJGehJyoEro6UhncgRw-fLw5m6MQ&gid=463183857"),
    ("erse_egme", 3, "https://docs.google.com/spreadsheets/d/1c1itP5vir1xZ9BkfJGehJyoEro6UhncgRw-fLw5m6MQ/export?format=csv&id=1c1itP5vir1xZ9BkfJGehJyoEro6UhncgRw-fLw5m6MQ&gid=1158313535"),
    ("erse_iec", 3, "https://docs.google.com/spreadsheets/d/1c1itP5vir1xZ9BkfJGehJyoEro6UhncgRw-fLw5m6MQ/export?format=csv&id=1c1itP5vir1xZ9BkfJGehJyoEro6UhncgRw-fLw5m6MQ&gid=2023046182")
]

def etl_gsheets():


    for name, header_index, url in GSHEETS_PAGES_URLS:
        
        print(f"Extraction sheet '{name}'...")

        # Extract sheet data
        r = requests.get(url)
        
        # Transform
        df = pd.read_csv(BytesIO(r.content), header=header_index)

        # Store locally
        os.makedirs("data", exist_ok=True)
        df.to_csv(os.path.join("data", name + ".csv"), index=False)


if __name__ == "__main__":
    etl_gsheets()
