import pandas as pd
import extract
import transform
import os
import dotenv


# load env vars from .env
dotenv.load_dotenv(dotenv.find_dotenv())

# Access the variables
TOKEN = os.getenv("API_TOKEN")
DB_ID = os.getenv("DB_ID")

# download data to data directory
extract.download_data(TOKEN, DB_ID)

# load calibration.csv
calibrate_df = pd.read_csv("data/calibration.csv")

# estimate epsilon from calibration data
out = transform.calibrate_beer_lambert(calibrate_df, "calibrate")
epsilon = transform.estimate_epsilon(out)

# array of countries
countries = ["Portugal", "Brazil", "Italy"]

# directory to read data from
directory = os.listdir("data/")

# calculate concentration for each of the files and write output table to results directory
for country in countries:
    files_to_load = [file for file in directory if country in file]
    files_to_load.sort()
    df_blank = pd.read_csv(f"data/{files_to_load[0]}")
    for file in files_to_load[1:]:
        df = pd.read_csv(f"data/{file}")
        out = transform.calculate_concentration(df, df_blank, epsilon)
        out.to_csv(f"results/{file}")
        print(f"file: {file}")
        print(f"mean concentration: {out['Concentration'].mean()}")