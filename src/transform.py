import pandas as pd
import numpy as np
import seaborn as sns

def melt_data(df):
    """
    Melt data from wide to long
    df: DataFrame
    """
    return pd.melt(df, id_vars=["Sample", "Dilution"], value_vars=df.columns[2:], var_name="Wavelength", value_name="Total_absorbance")

def calculate_mean_absorbance(df, name: str):
    """
    calculate mean of total absorbance and error
    df: DataFrame
    name: sample or blank
    """
    group = df.groupby(["Dilution", "Wavelength"])["Total_absorbance"].mean().reset_index()
    group.rename(columns={"Total_absorbance":"Mean_absorbance"}, inplace=True)
    group[f"Abs_error_{name}"] = (df.groupby(["Dilution", "Wavelength"])["Total_absorbance"].std()/np.sqrt(3)).reset_index()["Total_absorbance"]
    
    return group

def calculate_epsilon(df):
    """
    Calculate epsilon for calibration data
    df: Callibration DataFrame
    """
    # calculate epsilon
    df["Epsilon"] = df["Corrected_absorbance"]/df["Concentration"]
    return df

def calibrate_beer_lambert(df: pd.DataFrame, ) -> pd.DataFrame:
    """
    Calibrate a beer lambert curve using calibration data provided
    df: calibration dataframe
    name: name of dataframe
    """
    df = melt_data(df)

    # filter for S1 samples
    sample = df.loc[df["Sample"]=="S1"]

    # calculate mean of total absorbance and error
    grouped_sample = calculate_mean_absorbance(sample, "sample")

    # filter for blank samples
    blank = df.loc[df["Sample"]=="Blank"]

    # calculate mean of blank absorbance and error
    grouped_blank = calculate_mean_absorbance(blank, "blank")

    # merge sample and blank tables
    out = pd.merge(grouped_sample, grouped_blank[["Wavelength", "Mean_abs_blank"]], on="Wavelength")

    # calculate corrected absorbance and error
    out["Corrected_absorbance"] = out["Mean_absorbance"] - out["Mean_abs_blank"]
    out["Corrected_error"] = out["Abs_error_sample"] + out["Abs_error_blank"]

    # calculate concentration
    out = 50/out["Dilution"]

    # calculate epsilon
    out = calculate_epsilon(out)

    return out

def plot_abs_wavelength(df, name: str):
    # convert wavelength dtype to int
    df.Wavelength = df.Wavelength.astype(float).astype(int)

    # plot wavelength against corrected_absorbance
    g1 = sns.lineplot(df, x="Wavelength", y="Corrected_absorbance", hue="Dilution")

    # save figure to results directory
    # g1.figure.savefig(f"results/wavelength_absorbance_{name}.png")

    # zoom in on wavelength against corrected_absorbance
    g2 = sns.lineplot(df, x="Wavelength", y="Corrected_absorbance", hue="Dilution",)
    g2.set(
        xlim=(400, 600)
    )

    # save zoomed in plot
    # g2.figure.savefig(f"results/wavelength_absorbance_zoom_{name}.png")

def estimate_epsilon(df: pd.DataFrame) -> float:
    """
    Estimates the value of epsilon using calibration data
    df: calibration dataframe
    """
    # groupby concentration 
    df = df.groupby("Concentration")["Corrected_absorbance"].mean().reset_index()
    # calculate epsilon
    df = calculate_epsilon(df)
    # take final value, epsilon is gradient, making assumption that line cuts through 0,0
    # use final point and 0, 0 to calculate gradient/epsilon via formula (y2-y1)/(x2-x1)
    return df["Epsilon"].values[-1]

def calculate_concentration(sample: pd.DataFrame, blank: pd.DataFrame, epsilon:float) -> pd.DataFrame:
    """
    Calculate the concentration of each of the samples that were measured
    df: dataframe of the sample measurements
    df_blank: dataframe of the corresponding blank measurements
    epsilon: epsilon value obtained from calibration
    """
    # melt from wide to long
    sample = melt_data(sample)

    # melt from wide to long
    blank = melt_data(blank)

    # calculate mean of total absorbance and error
    grouped_sample = calculate_mean_absorbance(sample, "sample")

    # calculate mean of blank absorbance and error
    grouped_blank = calculate_mean_absorbance(blank, "blank")
    
    # merge sample and blank tables
    out = pd.merge(grouped_sample, grouped_blank[["Wavelength", "Mean_abs_blank"]], on="Wavelength")

    # calculate corrected absorbance and error
    out["Corrected_absorbance"] = out["Mean_absorbance"] - out["Mean_abs_blank"]
    out["Corrected_error"] = out["Abs_error_sample"] + out["Abs_error_blank"]

    # calculate concentration
    out["Concentration"] = out["Corrected_absorbance"] / epsilon
    
    return out