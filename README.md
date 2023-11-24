# Colorifix Technical Task

The goal of this technical test is to build a data pipeline that performs the following:
1. Access a remote data table containing fermentation data produced in dye houses using Colorifix's technology. The data should be accessed via a public API.
2. Calibrate a Beer-Lambert model to find the pigment concentration from absorbance data.
3. Collect absorbance data from 1. to calculate pigment concentrations for each data record using the model in 2.
4. Load the results into a structured dtabase and/or provide plots.

# Setup
1. clone the git repo
```
git clone https://github.com/EcoFiendly/colorifix_test.git
cd colorifix_test
```

2. create a .env file in the directory and store the token and database id in there in this format
```
API_TOKEN = your token here
```