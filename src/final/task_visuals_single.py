import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import pytask
import seaborn as sns

from src.config import BLD

sns.set(font_scale=1.5, style="white")

mobility = [
    "workplaces_percent_change_from_baseline",
    "transit_stations_percent_change_from_baseline",
    "residential_percent_change_from_baseline",
    "retail_and_recreation_percent_change_from_baseline",
]
index = ["E_index_score", "R_index_score", "S_index_score"]


def plot_visual_1(df, path):
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
        font=dict(size=15),
    )
    fig.write_image(str(pathlib.Path(path)), format="png")


def plot_visual_2(df, path):
    fig = px.line(
        df,
        x="date",
        y=[
            "E_index_score",
            "workplaces_percent_change_from_baseline",
            "transit_stations_percent_change_from_baseline",
            "residential_percent_change_from_baseline",
        ],
        title="Changes in Mobility vs. School Stringency Index over Time",
        width=1200,
        height=500,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Baseline Changes for Various Mobility Types, in %",
        legend_title="Legend",
        font=dict(size=15),
        template="simple_white",
    )
    fig.write_image(str(pathlib.Path(path)), format="png")


def plot_visual_3(df, path):
    count = 1
    plt.subplots(sharex=True, figsize=(30, 30))
    plt.suptitle(
        "Deviation in Mobility from Baseline According to Level of Contact Stringency",
        size=40,
    )
    for i in index:
        for t in mobility:
            plt.subplot(3, 4, count)
            sns.lineplot(x=df[i], y=df[t])
            count += 1
    plt.savefig(path)


@pytask.mark.parametrize(
    "produces,depends_on",
    [
        (
            {
                "visual_1": BLD / "figures" / "Stringency_index_over_time.png",
                "visual_2": BLD
                / "figures"
                / "Mobility_vs_education_sub_score_index.png",
                "visual_3": BLD / "figures" / "Mobility_vs_sub_score_indices.png",
            },
            BLD / "data" / "df_visuals.csv",
        )
    ],
)
def task_visuals_single(depends_on, produces):
    data = pd.read_csv(depends_on)
    plot_visual_1(data, produces["visual_1"])
    plot_visual_2(data, produces["visual_2"])
    plot_visual_3(data, produces["visual_3"])
