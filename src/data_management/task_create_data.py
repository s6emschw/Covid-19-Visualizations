import numpy as np
import pandas as pd
import pytask

from src.config import BLD
from src.config import SRC

cols = ["start_date", "end_date"]
start_cols = ["start_date", "row", "scale", "flag", "recorded_flag", "maximum"]
end_cols = start_cols[:]
del end_cols[0]
end_cols.extend(["end_date"])
wide_cols = start_cols[:]
del wide_cols[0:2]


def create_data(df, path):
    """Clean policy data.

    This function cleans and manages data to create 'covid_policy' data frame.

    Args:
        df (data frame): Original data in .csv format to be cleaned and managed.
        path           : Path under which resulting 'covid_policy' data frame is to be saved.

    Returns:
        data frame: covid_policy.csv is used for further analysis.

    """
    # Change datatypes
    for col in cols:
        df[col] = df[col].astype("datetime64[ns]")
    # Decompose data for every single day from 2020-02-01 to 2021-02-14 for each indicator
    df["row"] = range(len(df))
    starts = df[start_cols].rename(columns={"start_date": "date"})
    ends = df[end_cols].rename(columns={"end_date": "date"})
    df_decomp = pd.concat([starts, ends]).set_index("row", append=True)
    df_decomp = df_decomp.groupby(level=[0, 1]).apply(
        lambda x: x.set_index("date").resample("D").fillna(method="pad")
    )
    df_decomp.reset_index(inplace=True)
    # Long to wide format
    df_new = df_decomp.pivot(
        index="date",
        columns="indicator",
        values=wide_cols,
    )
    df_new.columns = ["_".join(col) for col in df_new.columns]
    # Fill missing values
    df_new.replace({-100: np.nan}, inplace=True)
    # Save the data
    return df_new.to_csv(path)


@pytask.mark.depends_on(SRC / "original_data" / "policy_data.csv")
@pytask.mark.produces(BLD / "data" / "covid_policy.csv")
def task_create_data(depends_on, produces):
    policy_data = pd.read_csv(depends_on).set_index("indicator")
    create_data(policy_data, produces)
