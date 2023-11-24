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

# Background
Beer-Lambert equation can be used to determine the relationship between absorbance (A) and concentration (c):
```
A = E c l
```
E is the absorptivity coefficient and l is optical path length in cm.
Assume when measuring multiple chemicals their absorbances can be added such that for N chemicals, A is the sum of absorbance of each of the chemicals. When measuring a sample in the spectrophotometer (chemical in a solvent), we also measure the solvent only (i.e. no pigment) and call this a Blank.