import pathlib

import pandas as pd
import plotly.express as px
import pytask
from plotly.subplots import make_subplots

from src.config import BLD


cols = ["new_cases_smoothed", "new_deaths_smoothed"]
titles = ["New Covid-19 Cases", "New Covid-19 Deaths"]
axes = [dict(range=[0, 30000]), dict(range=[0, 950])]


def plot_visual_6(df, path):
    for i, (col, title, axis) in enumerate(zip(cols, titles, axes)):
        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        fig = px.bar(
            df_visuals,
            x="date",
            y="stringency_index_score",
            color="stringency_index_score",
        )
        figi = px.line(df_visuals, x="date", y=col)
        figi.update_traces(yaxis="y2")
        subfig.add_traces(fig.data + figi.data)
        subfig.update_layout(
            width=1200,
            height=600,
            title="Comparing %s with Aggregate Stringency Index over Time" % title,
            font=dict(size=17),
        )
        subfig.update_layout(yaxis=dict(range=[0, 100]), yaxis2=axis)
        subfig.layout.xaxis.title = "Date"
        subfig.layout.yaxis.title = "Aggregate Stringency Index"
        subfig.layout.yaxis2.title = "%s" % title
        subfig.layout.legend.title = "Legend"
        subfig.layout.template = "simple_white"
        subfig.write_image(str(pathlib.Path(path)), format="png")


@pytask.mark.parametrize(
    "produces,depends_on",
    [
        (
            {"visual_6": BLD / "figures" / f"{title}_vs_stringency_index.png"},
            BLD / "data" / "df_visuals.csv",
        )
        for title in titles
    ],
)
def task_visual_6(depends_on, produces):
    data = pd.read_csv(depends_on)
    plot_visual_6(data, produces["visual_6"])
