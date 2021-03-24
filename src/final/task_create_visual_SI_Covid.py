import pathlib

import pandas as pd
import plotly.express as px
import pytask
from plotly.subplots import make_subplots

from src.config import BLD

corona_vars = ["new_cases_smoothed", "new_deaths_smoothed"]
colours = ["#547482", "#C87259"]
titles = ["New Covid-19 Cases", "New Covid-19 Deaths"]
axes = [dict(range=[0, 30000]), dict(range=[0, 950])]


def create_visual_SI_Covid(df, corona_var, colour, title, axis):
    """Create plots of Stringency Index (SI) and Corona related data over time.

    This function generates plots for new Covid deaths and new Covid cases
    and the Stringency Index. It shows the respective Covid related
    variable and Stringency Index at a given point in time.

    Args:
        df (data frame) : Data prepared for creating plots in .csv format.
        corona_var (int): Covid Data on new deaths and new cases for Germany.
        colour (str)    : Colours used in estimagic for visualizations.
        title (str)     : Names given to the axes and titles of the plots.
        axis (dict)     : Range for the secondary y axis.

    Returns:
        fig: Plots showing the change in Stringency Index and respective
             covid variables over time.

    """
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = px.bar(
        df, x="date", y="stringency_index_score", color="stringency_index_score"
    )
    figi = px.line(df, x="date", y=corona_var, color_discrete_sequence=[colour])
    figi.update_traces(yaxis="y2")
    subfig.add_traces(fig.data + figi.data)
    subfig.update_layout(
        width=1200,
        height=600,
        title="Comparing %s with Aggregate Stringency Index over Time" % title,
        title_x=0.5,
        title_font=dict(size=20),
    )
    subfig.update_layout(yaxis=dict(range=[0, 100]), yaxis2=axis)
    subfig.layout.xaxis.title = "Date"
    subfig.layout.yaxis.title = "Aggregate Stringency Index"
    subfig.layout.yaxis2.title = "%s" % title
    subfig.layout.template = "simple_white"
    return subfig


specifications = [
    (
        BLD / "data" / "df_visuals.csv",
        BLD / "figures" / f"{title}_vs_Stringency_Index.png",
        corona_var,
        colour,
        title,
        axis,
    )
    for corona_var, colour, title, axis in zip(corona_vars, colours, titles, axes)
]


@pytask.mark.parametrize(
    "depends_on,produces, corona_var,colour,title,axis", specifications
)
def task_create_visual_SI_Covid(depends_on, produces, corona_var, colour, title, axis):
    data = pd.read_csv(depends_on)
    fig = create_visual_SI_Covid(data, corona_var, colour, title, axis)
    fig.write_image(str(pathlib.Path(produces)), format="png")
