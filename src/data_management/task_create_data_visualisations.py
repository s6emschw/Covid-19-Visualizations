import pandas as pd
import pytask

from src.config import BLD
from src.config import SRC


@pytask.mark.parametrize(
    "depends_on, produces",
    [
        (
            {
                "index_data": BLD / "analysis" / "stringency_index_data.csv",
                "death_data": SRC / "original_data" / "death_data.csv",
                "mobility_data": SRC / "original_data" / "DE_Mobility_Report.csv",
            },
            BLD / "data" / "df_visuals.csv",
        )
    ],
)
def task_data_visualisations(depends_on, produces):
    # Read the data
    stringency_index = pd.read_csv(depends_on["index_data"])
    mobility_data = pd.read_csv(depends_on["mobility_data"])
    corona_data = pd.read_csv(depends_on["death_data"])
    # Select data from 15.2.2020 until 26.1.2021
    stringency_index = stringency_index.iloc[14:361]
    stringency_index = stringency_index[
        [
            "date",
            "R_index_score",
            "E_index_score",
            "S_index_score",
            "stringency_index_score",
        ]
    ]
    stringency_index.reset_index(inplace=True, drop=True)
    mobility_data = mobility_data.iloc[0:347]
    mobility_data = mobility_data[
        [
            "retail_and_recreation_percent_change_from_baseline",
            "grocery_and_pharmacy_percent_change_from_baseline",
            "transit_stations_percent_change_from_baseline",
            "workplaces_percent_change_from_baseline",
            "residential_percent_change_from_baseline",
        ]
    ]
    mobility_data.reset_index(inplace=True, drop=True)
    corona_data = corona_data.iloc[23267:23614]
    corona_data = corona_data[["new_cases_smoothed", "new_deaths_smoothed"]]
    corona_data.reset_index(inplace=True, drop=True)
    df_visuals = pd.concat([stringency_index, mobility_data, corona_data], axis=1)
    df_visuals["date"] = df_visuals["date"].astype("datetime64[ns]")
    # Save the data
    df_visuals.to_csv(produces)
