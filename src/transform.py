import pandas as pd
import numpy as np
import seaborn as sns

def calibrate_beer_lambert(df, name):
    # melt from wide to long
    df = pd.melt(df, id_vars=["Sample", "Dilution"], value_vars=df.columns[3:], var_name="Wavelength", value_name="Total_absorbance")

    # filter for S1 samples
    cal_sample = df.loc[df["Sample"]=="S1"]

    # calculate mean of total absorbance and error
    cal_sample_calc = cal_sample.groupby(["Dilution", "Wavelength"])["Total_absorbance"].mean().reset_index()
    cal_sample_calc.rename(columns={"Total_absorbance":"Mean_absorbance"}, inplace=True)

    # filter for blank samples
    cal_blank = df.loc[df["Sample"]=="Blank"]

    # calculate mean of blank absorbance and error
    cal_blank_calc = cal_blank.groupby(["Dilution", "Wavelength"])["Total_absorbance"].mean().reset_index()
    cal_blank_calc.rename(columns={"Total_absorbance":"Mean_abs_blank"}, inplace=True)

    # merge sample and blank tables
    out = pd.merge(cal_sample_calc, cal_blank_calc[["Wavelength", "Mean_abs_blank"]], on="Wavelength")

    # calculate corrected absorbance and error
    out["Corrected_absorbance"] = out["Mean_absorbance"] - out["Mean_abs_blank"]

    # convert wavelength dtype to int
    out.Wavelength = out.Wavelength.astype(float).astype(int)

    # plot wavelength against corrected_absorbance
    g1 = sns.lineplot(out, x="Wavelength", y="Corrected_absorbance", hue="Dilution")

    # save figure to results directory
    g1.figure.savefig(f"results/wavelength_absorbance_{name}.png")

    # zoom in on wavelength against corrected_absorbance
    g2 = sns.lineplot(out, x="Wavelength", y="Corrected_absorbance", hue="Dilution",)
    g2.set(
        xlim=(400, 600)
    )

    # save zoomed in plot
    g2.figure.savefig(f"results/wavelength_absorbance_zoom_{name}.png")

    # calculate concentration
    out["Concentration"] = 50/out["Dilution"]

    # calculate epsilon
    out["Epsilon"] = out["Corrected_absorbance"]/out["Concentration"]

    return out