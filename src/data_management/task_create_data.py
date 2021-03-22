import numpy as np
import pandas as pd
import pytask

from src.config import BLD
from src.config import SRC


@pytask.mark.depends_on(SRC / "original_data" / "policy_data.csv")
@pytask.mark.produces(BLD / "data" / "covid_policy.csv")
def task_create_data(depends_on, produces):
    # Read the data
    policy_data = pd.read_csv(depends_on).set_index("indicator")
    # Change datatypes
    for col in ["start_date", "end_date"]:
        policy_data[col] = policy_data[col].astype("datetime64[ns]")
    # Decompose data for every single day from 2020-02-01 to 2021-02-14 for each indicator
    policy_data["row"] = range(len(policy_data))
    starts = policy_data[
        ["start_date", "scale", "flag", "recorded_flag", "maximum", "row"]
    ].rename(columns={"start_date": "date"})
    ends = policy_data[
        ["end_date", "scale", "flag", "recorded_flag", "maximum", "row"]
    ].rename(columns={"end_date": "date"})
    policy_data_decomp = pd.concat([starts, ends]).set_index("row", append=True)
    policy_data_decomp = policy_data_decomp.groupby(level=[0, 1]).apply(
        lambda x: x.set_index("date").resample("D").fillna(method="pad")
    )
    policy_data_decomp.reset_index(inplace=True)
    # Long to wide format
    covid_policy = policy_data_decomp.pivot(
        index="date",
        columns="indicator",
        values=["scale", "flag", "recorded_flag", "maximum"],
    )
    covid_policy.columns = ["_".join(col) for col in covid_policy.columns]
    # Fill missing values
    covid_policy.replace({-100: np.nan}, inplace=True)
    # Save the data
    covid_policy.to_csv(produces)
