"""Creates plots that do not require looping"""
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import pytask
import seaborn as sns

from src.config import BLD

scores = ["E_index_score", "R_index_score", "S_index_score"]
mobility = [
    "workplaces_percent_change_from_baseline",
    "transit_stations_percent_change_from_baseline",
    "residential_percent_change_from_baseline",
    "retail_and_recreation_percent_change_from_baseline",
]
education = mobility[:]
del education[3]
education.extend(["E_index_score"])


def create_visual_SI_time(df):
    """Create plot of Stringency Index (SI) over time.

    This function generates plot for magnitude of
    Stringency Index over time.

    Args:
        df (data frame): Data prepared for creating plots in .csv format.

    Returns:
        fig: Plot showing the change in Stringency Index over time.

    """
    fig = px.bar(
        df,
        x="date",
        y="stringency_index_score",
        color="stringency_index_score",
        labels={"stringency_index_score": "Heat Magnitude"},
        title="Level of Aggregate Contact Stringency Index over Time",
        width=1000,
        height=600,
        template="simple_white",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Aggregate Stringency Index",
        legend_title="Aggregate Stringency Index",
        title_x=0.5,
        title_font=dict(size=20),
    )
    return fig


def create_visual_SSI_Mobility(df):
    """Create plots of Sub Score Indicies (SSI) vs Mobility Data.

    This function generates plots with four of the
    mobility variables versus the three Sub Score Indicies.
    Each subplot shows one of the mobility related
    variable versus one of the Sub Score Index.

    Args:
        df (data frame): Data prepared for creating plots in .csv format.

    Returns:
        fig: Plots showing the change in Sub Score Index as
             the mobility variable changes.

    """
    sns.set(font_scale=1.65, style="white")
    count = 1
    plt.subplots(figsize=(40, 30))
    plt.suptitle(
        "Deviation in Mobility from Baseline According to Level of Contact Stringency",
        size=50,
    )
    for i in scores:
        for t in mobility:
            plt.subplot(3, 4, count)
            sns.lineplot(x=df[i], y=df[t])
            count += 1
    return plt


def create_visual_ESSI_Mobility(df):
    """Create plots of Education Sub Score Index (ESSI) and Mobility Data over time.

    This function generates plot for three of the five mobility
    variables and the Education Sub Score Index. It shows the respective
    mobility related variable and Education Sub Score Index at a given point in time.

    Args:
        df (data frame): Data prepared for creating plots in .csv format.

    Returns:
        fig: Plots showing the change in Education Sub Score Index and
             mobility variables over time.

    """
    fig = px.line(
        df,
        x="date",
        y=education,
        title="Changes in Mobility vs. School Stringency Index over Time",
        width=1200,
        height=600,
        color_discrete_sequence=px.colors.qualitative.Antique,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Baseline Changes for Various Mobility Types, in %",
        legend_title="Legend:",
        title_x=0.5,
        title_font=dict(size=20),
        legend=dict(y=0.85, x=1),
        template="simple_white",
    )
    return fig


@pytask.mark.depends_on(
    BLD / "data" / "df_visuals.csv",
)
@pytask.mark.produces(
    {
        "visual_SI_time": BLD / "figures" / "Stringency_Index_over_time.png",
        "visual_SSI_Mobility": BLD / "figures" / "Mobility_vs_Sub_Score_indices.png",
        "visual_ESSI_Mobility": BLD
        / "figures"
        / "Mobility_vs_Education_Sub_Score_Index.png",
    }
)
def task_create_visuals(depends_on, produces):
    data = pd.read_csv(depends_on)
    fig = create_visual_SI_time(data)
    fig.write_image(str(pathlib.Path(produces["visual_SI_time"])), format="png")
    fig1 = create_visual_SSI_Mobility(data)
    fig1.savefig(produces["visual_SSI_Mobility"])
    fig2 = create_visual_ESSI_Mobility(data)
    fig2.write_image(str(pathlib.Path(produces["visual_ESSI_Mobility"])), format="png")
