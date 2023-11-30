import pandas as pd
import numpy as np
from src import transform

def test_melt_data():
    df = pd.DataFrame(
        {
            "Sample": ["S1", "S1", "S1", "S1"],
            "Dilution": [1, 1, 1, 1],
            200: [1, 1, 1, 1],
            222: [2, 2, 2, 2],
        }
    )

    expected = pd.DataFrame(
        {
            "Sample": ["S1", "S1", "S1", "S1", "S1", "S1", "S1", "S1"],
            "Dilution": [1, 1, 1, 1, 1, 1, 1, 1],
            "Wavelength": [200, 200, 200, 200, 222, 222, 222, 222],
            "Total_absorbance": [1, 1, 1, 1, 2, 2, 2, 2,]
        }
    )
    expected["Wavelength"] = expected["Wavelength"].astype(object)

    pd.testing.assert_frame_equal(transform.melt_data(df), expected)

def test_calculate_mean_absorbance():
    df = pd.DataFrame(
        {
            "Sample": ["S1", "S1", "S1", "S1", "S1", "S1", "S1", "S1"],
            "Dilution": [1, 1, 1, 1, 1, 1, 1, 1],
            "Wavelength": [200, 200, 200, 200, 222, 222, 222, 222],
            "Total_absorbance": [1, 1, 1, 1, 2, 2, 2, 2,]
        }
    )

    expected = pd.DataFrame(
        {
            "Dilution": [1, 1],
            "Wavelength": [200, 222],
            "Mean_absorbance": [1.0, 2.0],
            "Abs_error_test": [0.0, 0.0]
        }
    )

    pd.testing.assert_frame_equal(transform.calculate_mean_absorbance(df, "test"), expected)

def test_calculate_epsilon():
    df = pd.DataFrame(
        {
            "Corrected_absorbance": [1, 1],
            "Concentration": [50, 25],
        }
    )

    expected = pd.DataFrame(
        {
            "Corrected_absorbance": [1, 1],
            "Concentration": [50, 25],
            "Epsilon": [0.02, 0.04]
        }
    )

    pd.testing.assert_frame_equal(transform.calculate_epsilon(df), expected)

def test_estimate_epsilon():
    df = pd.DataFrame(
        {
            "Corrected_absorbance": [1, 1, 1],
            "Concentration": [50, 25, 12.5],
        }
    )
    
    expected = 0.02

    assert transform.estimate_epsilon(df) == expected