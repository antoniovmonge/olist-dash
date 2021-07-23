import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_table

from utils import Header, make_dash_table
from figures import *

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))


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
                                    The dataset has been anonymised.

                                    ❗ This dataset have already been filtered to only contain orders with a review.
                                    ''')
                            ),
                            html.Br(),
                            html.Br(),
                            html.Div(
                                [
                                    
                                    dcc.Markdown(
                                        """
                                        **Objective:** Increase customer satisfaction (so as to increase profit margin) while maintaining a healthy order volume.
                                        """),
                                    html.Br(),
                                ],
                                # className="product2",
                                # style=dict(textAlign='center')
                            ),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.H5(
                                        ["Payments"], className="subtitle padded"
                                    ),

                        ],
                        className='row'
                    ),
                    html.Div(
                        [
                            dcc.Markdown(
                            '''
                            ###### BRL: Brazilian real  
                            1 BRL = 0.1639 EUR
                            '''
                            )
                        ],
                        className='row'
                    ),
                    html.Div( # Row Payments
                        [
                            html.Div(
                                [
                                    dcc.Graph(
                                        figure=fig1(),
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className='six columns'
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        figure=payments_month(),
                                        config={"displayModeBar": False},
                                    )
                                ],
                                className='six columns'
                            )
                            
                        ],
                        className="row"
                    ),
                    html.Br(),
                    html.Div( # Row First Glimpse
                        [
                            html.Div( #Col1
                                [
                                    html.Div(
                                        [
                                            html.H5(
                                                ["First glimpse into Olist's business health"], className="subtitle padded"
                                            ),
                                        ],className='Row'
                                    ),
                                    
                                    html.Div(
                                        [
                                            dcc.Graph(
                                                figure=review_score(),
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className='nine columns'
                                    ),
                                    html.Div( # TABLE REVIEW SCORE
                                        [
                                            dash_table.DataTable(
                                            # id='table',
                                            # columns=[{"name": i, "id": i} for i in table_order_status().columns],
                                            columns=[{'name': 'Stars', 'id':'index'},{'name':'Count', 'id':'review_score'}],
                                            data=table_review_score().to_dict('records'),
                                            style_cell={
                                                'whiteSpace': 'normal',
                                                'height': 'auto',
                                                'textAlign': 'left',
                                                'padding': '5px'
                                            },
                                            style_header={
                                                'backgroundColor': 'white',
                                                'fontWeight': 'bold'
                                            },
                                            style_cell_conditional=[
                                                {
                                                    'if': {'column_id': 'review_score'},
                                                    'textAlign': 'right'
                                                }
                                            ],
                                            style_as_list_view=True,
                                            )
                                        ],
                                        className='three columns',
                                        style=dict(marginTop=100)
                                    ),
                                    
                                ],
                                className="six columns",
                            ),
                            html.Div( # COL ORDER STATUS
                                [
                                    html.Div(
                                        [
                                            html.H5(
                                                ["Order Status"], className="subtitle padded"
                                            ),
                                        ],className='Row'
                                    ),
                                    
                                    html.Div( #Col1
                                        [
                                            dcc.Graph(
                                                figure=order_status(),
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="nine columns",
                                    ),
                                    html.Div(
                                        [
                                            dash_table.DataTable(
                                            # id='table',
                                            # columns=[{"name": i, "id": i} for i in table_order_status().columns],
                                            columns=[{'name': 'Status', 'id':'index'},{'name':'Count', 'id':'order_status'}],
                                            data=table_order_status().to_dict('records'),
                                            style_cell={
                                                'whiteSpace': 'normal',
                                                'height': 'auto',
                                                'textAlign': 'left',
                                                'padding': '5px'
                                            },
                                            style_header={
                                                'backgroundColor': 'white',
                                                'fontWeight': 'bold'
                                            },
                                            style_as_list_view=True,
                                            style_cell_conditional=[
                                                {
                                                    'if': {'column_id': 'order_status'},
                                                    'textAlign': 'right'
                                                }
                                            ]
                                            )
                                        ],
                                        className='three columns',
                                        style=dict(marginTop=100)
                                    ),
                                ],
                                className="six columns",
                            ),
                            
                        ], className='row'
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(
                                        [
                                            'Customer Satisfaction'
                                        ],
                                        className="subtitle padded"
                                    ),
                                    dcc.Graph(
                                        figure=month_satisf(),
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className='six columns'
                            ),
                        
                        ],className='row'
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(
                                        ["Fund Facts"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(df_fund_facts)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H5(
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
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(
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
                                    html.H5(
                                        "Price & Performance (%)",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(df_price_perf)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H5(
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
