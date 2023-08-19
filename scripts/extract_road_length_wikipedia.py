import os
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

def extract():
    # get the response in the form of html
    wikiurl="https://en.wikipedia.org/wiki/List_of_countries_by_road_network_size"
    response=requests.get(wikiurl)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    roads_table=soup.find('table',{'class':"wikitable"})
    
    df = pd.read_html(str(roads_table))[0]
    
    # Cleaning
    df = df.rename(columns={
        'Total .mw-parser-output .nobold{font-weight:normal}(km)': 'Total',
        "Source & Year": "Year",
        "Paved (km)": "Paved",
        "Unpaved (km)": "Unpaved",
        "Controlled-access (km)": "Controlled_access",
    })

    df = df[[
        'Country', 'Total', 'Paved', 
        'Unpaved', 'Controlled_access', 'Year'
    ]]

    df = df.dropna(subset=["Country"])
    df["Country"] = df["Country"].str.replace("*", "").str.strip()
    df["Year"] = df.Year.str.findall(r'(?<!\d)\d{4}(?!\d)').str[0]

    # Cast
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
    df["Paved"] = pd.to_numeric(df["Paved"], errors="coerce")
    df["Unpaved"] = pd.to_numeric(df["Unpaved"], errors="coerce")
    df["Controlled_access"] = pd.to_numeric(df["Controlled_access"], errors="coerce")

    df.to_csv(
        os.path.join("notebooks/europe_comparison/rawdata", "roads_wikipedia.csv"),
        index=False
    )

if __name__ == "__main__":
    extract()
