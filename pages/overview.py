import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from utils import Header, make_dash_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))

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
            y=0.9,
            xanchor="center",
            x=0.05,
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
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Olist Store"),
                                    # html.Br([]),
                                    dcc.Markdown(
                                        """
                                        Olist Store is today among the largest online stores in the largest marketplaces in Brazil,\
                                        helping thousands of merchants to access the online commerce in an efficient and profitable way.\
                                        """,
                                        style={"color": "#ffffff"},
                                        # className="row",
                                    ),
                                ],
                                className="product",
                            ),
                            html.Div(
                                dcc.Markdown(
                                    '''
                                    **Data source:** [Kaggle Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce)  
                                      
                                    The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil.
                                    Its features allows viewing an order from multiple dimensions: from order status, price,
                                    payment and freight performance to customer location, product attributes and finally reviews written by customers.
                                    The dataset has been anonymised, and referenced to the companies and partners in the review text have been replaced
                                    with names of Game of Thrones great houses.
                                    ''')
                            ),
                        ],
                        className="row",
                    ),
                    # Row 3-4
                    html.Div(
                        [
                            html.H6(
                                        ["Overview"], className="subtitle padded"
                                    ),
                            dcc.Graph(
                                figure=fig,
                                config={"displayModeBar": False},
                    
                            ),


                        ],
                        className="twelve columns"
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Fund Facts"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(df_fund_facts)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Average annual performance",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=[
                                                        "1 Year",
                                                        "3 Year",
                                                        "5 Year",
                                                        "10 Year",
                                                        "41 Year",
                                                    ],
                                                    y=[
                                                        "21.67",
                                                        "11.26",
                                                        "15.62",
                                                        "8.37",
                                                        "11.11",
                                                    ],
                                                    marker={
                                                        "color": "#157E98",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="Calibre Index Fund",
                                                ),
                                                go.Bar(
                                                    x=[
                                                        "1 Year",
                                                        "3 Year",
                                                        "5 Year",
                                                        "10 Year",
                                                        "41 Year",
                                                    ],
                                                    y=[
                                                        "21.83",
                                                        "11.41",
                                                        "15.79",
                                                        "8.50",
                                                    ],
                                                    marker={
                                                        "color": "#dddddd",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="S&P 500 Index",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                # font={"family": "Raleway", "size": 10},
                                                height=350,
                                                width=600,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 10,
                                                    "l": 50,
                                                },
                                                showlegend=True,
                                                title="",
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 22.9789473684],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Hypothetical growth of $10,000",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=[
                                                        "2008",
                                                        "2009",
                                                        "2010",
                                                        "2011",
                                                        "2012",
                                                        "2013",
                                                        "2014",
                                                        "2015",
                                                        "2016",
                                                        "2017",
                                                        "2018",
                                                    ],
                                                    y=[
                                                        "10000",
                                                        "7500",
                                                        "9000",
                                                        "10000",
                                                        "10500",
                                                        "11000",
                                                        "14000",
                                                        "18000",
                                                        "19000",
                                                        "20500",
                                                        "24000",
                                                    ],
                                                    line={"color": "#97151c"},
                                                    mode="lines",
                                                    name="Calibre Index Fund Inv",
                                                )
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                title="",
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                width=340,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0277108433735,
                                                    "y": -0.142606516291,
                                                    "orientation": "h",
                                                },
                                                margin={
                                                    "r": 20,
                                                    "t": 20,
                                                    "b": 20,
                                                    "l": 50,
                                                },
                                                showlegend=True,
                                                xaxis={
                                                    "autorange": True,
                                                    "linecolor": "rgb(0, 0, 0)",
                                                    "linewidth": 1,
                                                    "range": [2008, 2018],
                                                    "showgrid": False,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                },
                                                yaxis={
                                                    "autorange": False,
                                                    "gridcolor": "rgba(127, 127, 127, 0.2)",
                                                    "mirror": False,
                                                    "nticks": 4,
                                                    "range": [0, 30000],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "ticklen": 10,
                                                    "ticks": "outside",
                                                    "title": "$",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                    "zerolinewidth": 4,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Price & Performance (%)",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(df_price_perf)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Risk Potential", className="subtitle padded"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("risk_reward.png"),
                                        className="risk-reward",
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
