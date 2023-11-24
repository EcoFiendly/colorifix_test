import dotenv
import os
import requests
import datetime
import gdown

def download_data(token, db_id):
    # Headers
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # Query the notion database
    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    r = requests.post(url, headers=headers)
    data = r.json()

    # Download files from gdrive and name accordingly, write to data/
    for i in range(len(data["results"])):
        # Parse the information from json
        sample_type = data["results"][i]["properties"]["Sample type"]["select"]["name"]
        client = data["results"][i]["properties"]["Client"]["select"]["name"][-1]
        client_location = data["results"][i]["properties"]["Client location"]["select"]["name"]
        fermentor_used = data["results"][i]["properties"]["Fermentor used"]["select"]["name"][-1]
        fermentor_model = data["results"][i]["properties"]["Fermentor model"]["select"]["name"][-1]
        date = datetime.datetime.fromisoformat(data["results"][i]["properties"]["Date"]["date"]["start"]).strftime("%Y%m%d_%H%M")
        url = data["results"][i]["properties"]["Download URL"]["url"]

        # create name of file
        file_name = f"{sample_type}_{client}_{client_location}_{fermentor_used}_{fermentor_model}_{date}.csv"
        
        # download the file and write to data directory
        gdown.download(url, f"data/{file_name}", quiet=False)