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

# Thought process
1. for calibration data:
    1. since A = E c l and l = 1cm, equation can be written as A = E c
    2. using the calibration data, and having A and c, equation can be rewritten as E = A/c
    3. to obtain A(pigment), I need to first subtract A(blank) from A(total)
    3. plug in A(pigment) and c from calibration data and get E
2. Taking the E from calibration and calculating concentration for each of the samples:
    1. we now need to find c, equation can be rewritten as c = A/E
    2. once again need to subtract A(blank) from A(total)
    3. plug in A(pigment) and E to get c