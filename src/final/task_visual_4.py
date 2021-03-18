import pathlib

import pandas as pd
import plotly.express as px
import pytask

from src.config import BLD


baselines = [
    "retail_and_recreation_percent_change_from_baseline",
    "grocery_and_pharmacy_percent_change_from_baseline",
    "transit_stations_percent_change_from_baseline",
    "workplaces_percent_change_from_baseline",
    "residential_percent_change_from_baseline",
]
titles = [
    "Retail and Recreation",
    "Grocery and Pharmacy",
    "Transit Stations",
    "Workplaces",
    "Residential",
]
colours = ["blue", "green", "yellow", "maroon", "navy"]


def plot_visual_4(df, path):
    for i, (baseline, title, colour) in enumerate(zip(baselines, titles, colours)):
        figi = px.line(
            df,
            x="date",
            y=[baseline, "stringency_index_score"],
            title="Comparison of %s Mobility Trend with Aggregate Stringency Index over Time"
            % title,
            width=1200,
            height=700,
            color_discrete_sequence=[colour, "red"],
            template="simple_white",
        )
        figi.update_layout(
            xaxis_title="Date",
            yaxis_title="Baseline Change for %s Mobility, in %%" % title,
            legend_title="Legend",
            font=dict(size=15),
        )
        figi.write_image(str(pathlib.Path(path)), format="png")


@pytask.mark.parametrize(
    "produces,depends_on",
    [
        (
            {"visual_4": BLD / "figures" / f"{title}_mobility_vs_stringency_index.png"},
            BLD / "data" / "df_visuals.csv",
        )
        for title in titles
    ],
)
def task_visual_4(depends_on, produces):
    data = pd.read_csv(depends_on)
    plot_visual_4(data, produces["visual_4"])
