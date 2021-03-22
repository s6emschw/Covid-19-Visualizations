import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import pytask
import seaborn as sns
from plotly.subplots import make_subplots

from src.config import BLD


mobility = [
    "workplaces_percent_change_from_baseline",
    "transit_stations_percent_change_from_baseline",
    "residential_percent_change_from_baseline",
    "retail_and_recreation_percent_change_from_baseline",
]
baselines = mobility[:]
baselines.extend(["grocery_and_pharmacy_percent_change_from_baseline"])
education = mobility[:]
del education[3]
education.extend(["E_index_score"])
scores = ["E_index_score", "R_index_score", "S_index_score"]
titles_1 = ["Schools", "Private Gatherings", "Public Activities"]
titles_2 = [
    "Workplaces",
    "Transit Stations",
    "Residential",
    "Retail and Recreation",
    "Grocery and Pharmacy",
]
titles_3 = ["New Covid-19 Cases", "New Covid-19 Deaths"]
corona = ["new_cases_smoothed", "new_deaths_smoothed"]
colours = ["#547482", "#C87259", "#F1B05D", "#7A8C87", "#C8B05C"]
axes = [dict(range=[0, 30000]), dict(range=[0, 950])]


def plot_visual_1(df, i, path):
    fig = px.line(
        df,
        x="date",
        y=scores[i],
        title="Level of Contact Stringency for %s over Time" % titles_1[i],
        width=1000,
        height=600,
        template="simple_white",
        color_discrete_sequence=[colours[i]],
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="%s Stringency Index" % titles_1[i],
        title_x=0.5,
        title_font=dict(size=20),
    )
    fig.write_image(str(pathlib.Path(path)), format="png")


def plot_visual_2(df, path):
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
    fig.write_image(str(pathlib.Path(path)), format="png")


def plot_visual_3(df, path):
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
    plt.savefig(path)


def plot_visual_4(df, i, path):
    fig = px.line(
        df,
        x="date",
        y=[baselines[i], "stringency_index_score"],
        title="Comparison of %s Mobility Trend with Aggregate Stringency Index over Time"
        % titles_2[i],
        width=1200,
        height=600,
        color_discrete_sequence=[colours[i], "#3C2030"],
        template="simple_white",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Baseline Change for %s Mobility, in %%" % titles_2[i],
        legend_title="Legend:",
        legend=dict(y=0.75, x=1),
        title_x=0.5,
        title_font=dict(size=20),
    )
    fig.write_image(str(pathlib.Path(path)), format="png")


def plot_visual_5(df, path):
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
    fig.write_image(str(pathlib.Path(path)), format="png")


def plot_visual_6(df, i, path):
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = px.bar(
        df, x="date", y="stringency_index_score", color="stringency_index_score"
    )
    figi = px.line(df, x="date", y=corona[i], color_discrete_sequence=[colours[i]])
    figi.update_traces(yaxis="y2")
    subfig.add_traces(fig.data + figi.data)
    subfig.update_layout(
        width=1200,
        height=600,
        title="Comparing %s with Aggregate Stringency Index over Time" % titles_3[i],
        title_x=0.5,
        title_font=dict(size=20),
    )
    subfig.update_layout(yaxis=dict(range=[0, 100]), yaxis2=axes[i])
    subfig.layout.xaxis.title = "Date"
    subfig.layout.yaxis.title = "Aggregate Stringency Index"
    subfig.layout.yaxis2.title = "%s" % titles_3[i]
    subfig.layout.template = "simple_white"
    subfig.write_image(str(pathlib.Path(path)), format="png")


@pytask.mark.parametrize(
    "produces,depends_on",
    [
        (
            {
                "visual_1_0": BLD / "figures" / "Stringency_Index_for_Schools.png",
                "visual_1_1": BLD
                / "figures"
                / "Stringency_Index_for_Private_Gatherings.png",
                "visual_1_2": BLD
                / "figures"
                / "Stringency_Index_for_Public_Activities.png",
                "visual_2": BLD / "figures" / "Stringency_Index_over_time.png",
                "visual_3": BLD / "figures" / "Mobility_vs_Sub_Score_indices.png",
                "visual_4_0": BLD
                / "figures"
                / "Retail_Recreation_mobility_vs_Stringency_Index.png",
                "visual_4_1": BLD
                / "figures"
                / "Grocery_Pharmacy_mobility_vs_Stringency_Index.png",
                "visual_4_2": BLD
                / "figures"
                / "Transit_Stations_mobility_vs_Stringency_Index.png",
                "visual_4_3": BLD
                / "figures"
                / "Workplaces_mobility_vs_Stringency_Index.png",
                "visual_4_4": BLD
                / "figures"
                / "Residential_mobility_vs_Stringency_Index.png",
                "visual_5": BLD
                / "figures"
                / "Mobility_vs_Education_Sub_Score_Index.png",
                "visual_6_0": BLD
                / "figures"
                / "Covid-19_Cases_vs_Stringency_Index.png",
                "visual_6_1": BLD
                / "figures"
                / "Covid-19_Deaths_vs_Stringency_Index.png",
            },
            BLD / "data" / "df_visuals.csv",
        )
    ],
)
def task_visualizations(depends_on, produces):
    data = pd.read_csv(depends_on)
    plot_visual_1(data, 0, produces["visual_1_0"])
    plot_visual_1(data, 1, produces["visual_1_1"])
    plot_visual_1(data, 2, produces["visual_1_2"])
    plot_visual_2(data, produces["visual_2"])
    plot_visual_3(data, produces["visual_3"])
    plot_visual_4(data, 0, produces["visual_4_0"])
    plot_visual_4(data, 1, produces["visual_4_1"])
    plot_visual_4(data, 2, produces["visual_4_2"])
    plot_visual_4(data, 3, produces["visual_4_3"])
    plot_visual_4(data, 4, produces["visual_4_4"])
    plot_visual_5(data, produces["visual_5"])
    plot_visual_6(data, 0, produces["visual_6_0"])
    plot_visual_6(data, 1, produces["visual_6_1"])
