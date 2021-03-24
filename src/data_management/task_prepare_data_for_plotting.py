import pandas as pd
import pytask

from src.config import BLD
from src.config import SRC

stringency_data_cols = [
    "date",
    "R_index_score",
    "E_index_score",
    "S_index_score",
    "stringency_index_score",
]
mobility_data_cols = [
    "retail_and_recreation_percent_change_from_baseline",
    "grocery_and_pharmacy_percent_change_from_baseline",
    "transit_stations_percent_change_from_baseline",
    "workplaces_percent_change_from_baseline",
    "residential_percent_change_from_baseline",
]
corona_data_cols = ["new_cases_smoothed", "new_deaths_smoothed"]


def prepare_data_for_plotting(stringency_data, mobility_data, corona_data, path):
    """Prepare data for visualisations.

    This function selects parts of different datasets and concats them to
    create 'df_visuals' data frame.

    Args:
        stringency_data (data frame): Cleaned data with Stringency indicies in .csv format.
        mobility_data (data frame)  : Google Mobility data for Germany in .csv format.
        corona_data (data frame)    : Data on Covid related cases and deaths in .csv format.
        path                        : Path under which resulting 'df_visuals'
                                      data frame is to be saved.

    Returns:
        data frame: df_visuals.csv is used for creating visualisations.

    """
    # Select data from 15.2.2020 until 26.1.2021 in stringency index data
    stringency_data = stringency_data.iloc[14:361]
    stringency_data = stringency_data[stringency_data_cols]
    stringency_data.reset_index(inplace=True, drop=True)
    # Select data from 15.2.2020 until 26.1.2021 in mobility data
    mobility_data = mobility_data.iloc[0:347]
    mobility_data = mobility_data[mobility_data_cols]
    mobility_data.reset_index(inplace=True, drop=True)
    # Select data from 15.2.2020 until 26.1.2021 in corona data
    corona_data = corona_data.iloc[23267:23614]
    corona_data = corona_data[corona_data_cols]
    corona_data.reset_index(inplace=True, drop=True)
    # Concat the datasets
    df_visuals = pd.concat([stringency_data, mobility_data, corona_data], axis=1)
    df_visuals["date"] = df_visuals["date"].astype("datetime64[ns]")
    # Save the data
    return df_visuals.to_csv(path)


@pytask.mark.parametrize(
    "depends_on, produces",
    [
        (
            {
                "stringency_data": BLD / "analysis" / "stringency_index_data.csv",
                "corona_data": SRC / "original_data" / "death_data.csv",
                "mobility_data": SRC / "original_data" / "DE_Mobility_Report.csv",
            },
            BLD / "data" / "df_visuals.csv",
        )
    ],
)
def task_prepare_data_for_plotting(depends_on, produces):
    stringency_data = pd.read_csv(depends_on["stringency_data"])
    mobility_data = pd.read_csv(depends_on["mobility_data"])
    corona_data = pd.read_csv(depends_on["corona_data"])
    prepare_data_for_plotting(stringency_data, mobility_data, corona_data, produces)
