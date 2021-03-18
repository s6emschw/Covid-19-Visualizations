import pathlib

import pandas as pd
import plotly.express as px
import pytask

from src.config import BLD


def plot_visual_1(df, scores, titles, path):
    for i, (score, title) in enumerate(zip(scores, titles)):
        figi = px.line(
            df,
            x="date",
            y=score,
            title="Level of Contact Stringency for %s over Time" % title,
            width=1000,
            height=600,
            template="simple_white",
        )
        figi.update_layout(
            xaxis_title="Date",
            yaxis_title="%s Stringency Index" % title,
            font=dict(size=20),
        )
        figi.write_image(str(pathlib.Path(path)), format="png")


@pytask.mark.parametrize(
    "produces,depends_on",
    [
        (
            {BLD / "figures" / f"Stringency_index_for_{title}.png"},
            BLD / "data" / "df_visuals.csv",
        )
        for title in ["Schools", "Private Gatherings", "Public Activities"]
    ],
)
def task_visual_1(depends_on, produces):
    data = pd.read_csv(depends_on)
    scores = ["E_index_score", "R_index_score", "S_index_score"]
    titles = ["Schools", "Private Gatherings", "Public Activities"]
    plot_visual_1(data, scores, titles, produces)
