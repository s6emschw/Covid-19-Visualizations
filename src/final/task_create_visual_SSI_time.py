import pathlib

import pandas as pd
import plotly.express as px
import pytask

from src.config import BLD

scores = ["E_index_score", "R_index_score", "S_index_score"]
titles = ["Schools", "Private Gatherings", "Public Activities"]


def create_visual_SSI_time(df, score, title):
    """Create plots of Sub Score Indicies (SSI) over time.

    This function generates plots for each of the three Sub Score Indicies namely
    stringency index for containment policies for schools (E_index_score),
    stringency index for containment policies for public gatherings (R_index_score) and
    stringency index for containment policies for entertainment and shopping (S_index_score).
    It shows the respective Sub Score Index at a given point in time.

    Args:
        df (data frame): Data prepared for creating plots in .csv format.
        score (int)    : A value between 0 and 100 with 0 indicating no policy
                         restriction in place and 100 indicating the highest
                         level of stringency a policy can take on.
        title (str)    : Names given to the axes and titles of the plots.

    Returns:
        fig: Plots showing the change in Sub Score Indicies over time.

    """
    fig = px.line(
        df,
        x="date",
        y=score,
        title="Level of Contact Stringency for %s over Time" % title,
        width=1000,
        height=600,
        template="simple_white",
        color_discrete_sequence=px.colors.qualitative.Antique,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="%s Stringency Index" % title,
        title_x=0.5,
        title_font=dict(size=20),
    )
    return fig


specifications = [
    (
        BLD / "data" / "df_visuals.csv",
        BLD / "figures" / f"Stringency_Index_for_{title}.png",
        score,
        title,
    )
    for score, title in zip(scores, titles)
]


@pytask.mark.parametrize("depends_on,produces, score, title", specifications)
def task_create_visual_SSI_time(depends_on, produces, score, title):
    data = pd.read_csv(depends_on)
    fig = create_visual_SSI_time(data, score, title)
    fig.write_image(str(pathlib.Path(produces)), format="png")
