import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from utils import Header, make_dash_table

import pandas as pd
import pathlib

# LOAD DATA FRAME FROM AWS S3
# url='s3://psycovid/cleaned_data_040321.csv'

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../raw_data/csv").resolve()

# get the data
from olistdash.data import Olist
data = Olist().get_data()

df = data['order_payments'][['order_id','payment_value']].merge(data['orders'][['order_id','order_purchase_timestamp']], on='order_id', how='outer')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df = df.set_index('order_purchase_timestamp').sort_index()
df_daily = pd.DataFrame(df.resample('D')['payment_value'].sum()).reset_index()
df_daily = df_daily[df_daily['order_purchase_timestamp'] <= '2018-07-31']


fig = go.Figure(
    [
        go.Scatter(
            x=df_daily["order_purchase_timestamp"],
            y=df_daily["payment_value"],
            line=dict(color = "#DE3562"),
            name="Payments",
        )
    ]
)
# fig.add_trace(
#     go.Scatter(
#         x=df_dayly["Date"],
#         y=df_dayly["MSCI EAFE Index Fund (ETF)"],
#         line={"color": "#35CDDE"},
#         name="MSCI EAFE Index Fund (ETF)"
#     )
# )
fig.update_layout(
    autosize=True,
#                 width=700,
#                 height=200,
#                 font=dict(
#                     family="Lato, Sans-Serif",
#                     size= 10
#                     ),
    showlegend = True,
    hovermode  = 'x',
    margin={
        "r": 30,
        "t": 30,
        "b": 30,
        "l": 30,
    },
    legend=dict(
            yanchor="top",
            y=1.4,
            xanchor="center",
            x=0.5,
            font=dict(
                size=12,
            )
        ),
#                 titlefont=dict(
#                     family="Lato, Sans-Serif",
#                     size= 10
#                     ),
    xaxis={
        "autorange": True,
#                     "range": [
#                         "2007-12-31",
#                         "2018-08-31",
#                     ],
        "rangeselector": {
            "buttons": [
                {
                    "count": 1,
                    "label": "1M",
                    "step": "month",
                    "stepmode": "backward",
                },
                {
                    "count": 3,
                    "label": "3M",
                    "step": "month",
                    "stepmode": "backward",
                },
                {
                    "count": 6,
                    "label": "6M",
                    "step": "month",
                    "stepmode": "backward",
                },
                {
                    "count": 1,
                    "label": "1Y",
                    "step": "year",
                    "stepmode": "backward",
                },
                {
                    "label": "All",
                    "step": "all",
                },
            ]
        },
        'rangeslider':{'visible': True},
        "showline": True,
        "type": "date",
        "zeroline": False,
    },
    yaxis={
        "autorange": True,
        # "range": [
        #     18.6880162434,
        #     278.431996757,
        # ],
        "showline": True,
        "type": "linear",
        "zeroline": False,
    },
)


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    dcc.Graph(
                        figure=fig,
                        config={"displayModeBar": False},
                    
                    )
                ],
                className="twelve columns"
            ),
        ],
        className="page",
    )
