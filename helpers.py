import plotly.io as pio
from datetime import datetime
import pandas as pd
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import warnings
import re
import seaborn as sb

warnings.filterwarnings("ignore")


def isnull(df):
    for col in df.columns:
        print(f"The number of NaNs in {col}:", df[col].isnull().sum())


def get_top(df, col, n, column_name, count_name):
    """
    A function return neat df to be plotted (count categorical values)
    Args:
        - df--> data frame
        - col --> ctegorical values column.
        - n --> number of records to show (0 --> means all)
        - column_name --> categorical value to be named
        - count_name --> count column name
    Return:
        - df of two columns (categorical values and counter)
    """
    if n != 0:
        return (
            df[col]
            .value_counts()
            .head(n)
            .to_frame()
            .reset_index()
            .rename(columns={"index": column_name, col: count_name})
        )
    else:
        return (
            df[col]
            .value_counts()
            .to_frame()
            .reset_index()
            .rename(columns={"index": column_name, col: count_name})
        )


def pie(df, title):
    """
    A function to plot pie graph
    Args:
        - df--> DataFrame.
        - title --> the graph title
    """

    colors = px.colors.qualitative.T10

    fig = px.pie(
        df,
        values=f"{df.columns[1]}",
        names=f"{df.columns[0]}",
        color_discrete_sequence=colors,
        title=title,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label+value",
        textfont=dict(size=12, color="white"),
    )
    fig.show("svg")


def bar(df, x, y, title, text=0, margin=np.inf):
    """
    A function to plot bar graph
    Args:
        - df--> DataFrame.
        - x --> x axis values.
        - y --> y axis values.
        - text --> values for text.
        - margin --> margin value.
        - title --> the graph title.
    """
    if text == 0:
        text = y
    fig = px.bar(df, x=f"{x}", y=f"{y}", text=f"{y}", title=title)

    fig.update_layout(xaxis=dict(title=f"{x}", tickmode="linear", dtick=1))

    clrs = ["red" if (y > margin) else "#5296dd" for y in df[f"{y}"]]

    fig.update_traces(
        marker_color=clrs, marker_line_width=1.5, opacity=1, textposition="auto"
    )
    fig.show("svg")


def barh(df, title, threshold=float("inf"), c=0):
    """
    A function to plot barh graph
    Args:
        - df--> DataFrame.
        - title --> the graph title.
        - threshold --> plot in red if excced the value.
    """
    clrs = ["red" if (y > threshold) else "#5296dd" for y in df[f"{df.columns[1]}"]]

    fig = (
        px.bar(
            df,
            y=f"{df.columns[0]}",
            x=f"{df.columns[1]}",
            text=f"{df.columns[1]}",
            height=500,
            title=title,
        )
        .update_traces(marker_color=c if c != 0 else clrs)
        .update_layout()
    )

    fig.update_yaxes(autorange="reversed")
    fig.show("svg")


def bar_peaks(df_head, title):
    """
    A function to plot bar graph for peaks
    Args:
        - df_head -->  dataframe contains top values.
        - title --> the graph title.
    """
    fig = px.bar(df_head, x=f"{df_head.columns[0]}", y=f"{df_head.columns[1]}", 
                 text=f"{df_head.columns[1]}", title=title)

    fig.update_layout(
        xaxis=dict(
            title="Comments Creation Date", tickmode="array", tickvals=df_head.date
        )
    )

    fig.update_traces(marker_color="red", opacity=1, textposition="auto")
    fig.update_xaxes(tickangle=45)
    fig.show("svg")

    
def bar_dates(df, title, threshold=float("inf")):
    fig = px.bar(df, x="date", y="ncomments", text="ncomments")

    fig.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center", "yanchor": "top"}
    )
    fig.update_layout(xaxis=dict(title="Comments Creation Date", tickmode="linear"))

    clrs = ["red" if (y > threshold) else "#5296dd" for y in df["ncomments"]]
    fig.update_traces(
        marker_color=clrs, marker_line_width=1.5, opacity=1, textposition="auto"
    )
    fig.update_xaxes(tickangle=45)
    fig.show("svg")
    

def draw_heatmap(*args, **kwargs):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = kwargs.pop('data')
    d = data.pivot(index=args[1], columns=args[0], values=args[2])
    d = d.reindex(index=months[::-1])
    sb.heatmap(d, **kwargs)
    

def facet_heat(df, title='title', n_col=2, vmax=100):
    g = sb.FacetGrid(df, col='year', col_wrap=n_col, height=4.5)
    g.map_dataframe(draw_heatmap, 'dayofmonth', 'month', 'ncomments', cmap='rocket_r', vmin=0, vmax=vmax);

    plt.suptitle(title, y=1.06, fontsize=18)
    g.fig.subplots_adjust(wspace=0.15, hspace=0.2)
    for axis in g.axes.flat:
        axis.tick_params(labelbottom=True, labelleft=True)
    
    
def facet_day_month(df, x, y, facet_on='month', n_col=4, year_str='2018'):
    """
    A function to plot bar graph for all months
    Args:
        - df -->  dataframe.
    """
    months_ordered = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    days_ordered = list(range(1, 32, 2))

    g = sb.FacetGrid(data=df, col=facet_on, col_wrap=n_col, col_order=months_ordered if facet_on=='month' else None)
    g.map(sb.barplot, x, y, 
          order=days_ordered if facet_on=='month' else months_ordered, 
          palette=["#5296dd"])
    
    g.set_xticklabels(rotation=90)
    g.set_titles("{col_name}", size=14, y=-0.28)
    
    if facet_on=='month':
        title = "Comments Created in Each Day of " + year_str 
    else:
        title = "Comments Created in Each Month"
    g.fig.suptitle(title, fontsize=18, y=1.05)

    g.fig.subplots_adjust(wspace=0.1, hspace=0.3)
    g.set_xlabels("")
    for axis in g.axes.flat:
        axis.tick_params(labelbottom=True)


def get_amber_text(row):
    """
    A function to get texts related to amber.
    Args:
        - row -->  row of column in df.
    """
    row = row.lower()
    result = list(set(re.findall(r"#?[a-z\s]*amber[a-z\s]*", row)))
    neat = []
    for i in result:
        neat.append(i.strip())
    return neat


class SameText:
    def __init__(self, df, token):
        self.token_df = df[df.tokens == token]
        self.token = token

    def n_commnets_unique(self):
        print(
            f"This comment appeared in {self.token_df.message.value_counts().shape[0]} shape"
        )

    def get_df(self):
        return self.token_df

    def users(self):
        return self.token_df.username.value_counts()

    def dates(self):
        return self.token_df.date.value_counts()

    def head(self, n):
        return self.token_df.head(n)

    def shapes(self, n):
        return self.token_df.message.value_counts().head(n)

    def peak(self, n):
        bar_peaks(
            self.dates()
            .to_frame()
            .reset_index()
            .head(n)
            .rename(columns={"date": "n_comments"})
            .rename(columns={"index": "date"}),
            f"Peak Dates for {self.token}",
        )

    def date_info(self):
        min = self.dates().index.min()
        max = self.dates().index.max()
        print(f"The commentes were made between {min} and  {max}")
        print(
            self.token_df.groupby("year")
            .count()["message"]
            .to_frame()
            .rename(columns={"message": "n_comments"})
        )
        pie(
            self.token_df.groupby("year").count()["message"].to_frame().reset_index(),
            "Numner of Comments Per Year",
        )

        facet_heat(self.token_df, title='Numner of Comments Per Day')
        
        for year in self.token_df.year.unique():
            facet_days(self.token_df, str(int(year)))

    def users_dates(self, n):
        return (
            self.token_df.groupby(["username", "date"])
            .count()["message"]
            .sort_values(ascending=False)
            .head(n)
        )

    def df_timing(self):
        df = self.get_df()
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")
        df["diff"] = df.datetime.diff()
        return pd.concat([df, df["diff"].dt.components.iloc[:, 0:3]], axis=1)

    def get_groups(self, date):
        df = self.df_timing()
        return set(
            df[(df.days == 0) & (df.hours == 0) & (df.date.astype(str) == date)]
            .username.value_counts()
            .index
        )

