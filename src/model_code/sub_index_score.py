# import pandas as pd


class sub_index_code:

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


def calculate_sub_index_score(df, policy_value, flag, recorded_flag, maximum):
    numerator = df[policy_value] - 0.5 * (df[flag] - df[recorded_flag])
    denominator = df[maximum]
    return 100 * (numerator / denominator)
