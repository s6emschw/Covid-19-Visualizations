import pandas as pd
import pytask

from src.config import BLD


def calculate_sub_index_score(df, policy_value, flag, recorded_flag, maximum):
    """Sub Index Score calculates stringency level for each policy category.
    Inputs:
        policy_value (integer)  = ordinal scale measurement that represents level of policy
                                  stringency.
        flag (integer)          = dummy variable indicating whether or not an indicator
                                  uses a flag to distinguish between regionally and federally
                                  employed policies.
        recorded_flag (integer) = dummy variable indicating whether the policy is implemented
                                  regionally or federally.
        maximum (integer)       = maximum ordinal scale value each indicator can take.
    For further descriptions on inputs, see code book.
    Output:
        Output for calculate_sub_index_score is a value between 0 and 100 with 0 indicating no
        policy restriction in place and 100 indicating the highest level of stringency a policy
        can take on.
    """
    numerator = df[policy_value] - 0.5 * (df[flag] - df[recorded_flag])
    denominator = df[maximum]
    return 100 * (numerator / denominator)


new_cols_1 = [
    "SI_E1",
    "SI_E2",
    "SI_E3",
    "SI_E4",
    "R_index_score",
    "SI_S1",
    "SI_S2",
    "SI_S3",
    "SI_S4",
]
scale_cols = [
    "scale_E1",
    "scale_E2",
    "scale_E3",
    "scale_E4",
    "scale_R1",
    "scale_S1",
    "scale_S2",
    "scale_S3",
    "scale_S4",
]
flag_cols = [
    "flag_E1",
    "flag_E2",
    "flag_E3",
    "flag_E4",
    "flag_R1",
    "flag_S1",
    "flag_S2",
    "flag_S3",
    "flag_S4",
]
record_cols = [
    "recorded_flag_E1",
    "recorded_flag_E2",
    "recorded_flag_E3",
    "recorded_flag_E4",
    "recorded_flag_R1",
    "recorded_flag_S1",
    "recorded_flag_S2",
    "recorded_flag_S3",
    "recorded_flag_S4",
]
max_cols = [
    "maximum_E1",
    "maximum_E2",
    "maximum_E3",
    "maximum_E4",
    "maximum_R1",
    "maximum_S1",
    "maximum_S2",
    "maximum_S3",
    "maximum_S4",
]
new_cols_2 = ["E_index_score", "S_index_score", "stringency_index_score"]
subscore_cols = [new_cols_1[0:4], new_cols_1[5:9], new_cols_1]


@pytask.mark.depends_on(BLD / "data" / "covid_policy.csv")
@pytask.mark.produces(BLD / "analysis" / "stringency_index_data.csv")
def task_create_index(depends_on, produces):
    stringency_index_data = pd.read_csv(depends_on).set_index("date")
    for a, b, c, d, e in zip(new_cols_1, scale_cols, flag_cols, record_cols, max_cols):
        stringency_index_data[a] = calculate_sub_index_score(
            stringency_index_data, b, c, d, e
        )
    for i, j in zip(new_cols_2, subscore_cols):
        stringency_index_data[i] = stringency_index_data[j].mean(axis=1)
    stringency_index_data.to_csv(produces)
