import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_table
import numpy as np

from utils import Header, make_dash_table
from figures import *

import pandas as pd
import pathlib

# get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../data").resolve()


# df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
# df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))


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
                                    html.H4("Olist Store"),
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
                                    # html.Br(),
                                ],
                                # className="product2",
                                # style=dict(textAlign='center')
                            ),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.H4(
                                        ["REVENUE"], className="subtitle padded"
                                    ),

                        ],
                        className='row'
                    ),
                    html.Div(
                        [
                            dcc.Markdown(
                            '''
                            ###### *BRL: Brazilian real  
                            1 BRL = 0.1639 EUR
                            '''
                            ),
                            html.Br()
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
                                            html.H4(
                                                ["Review Scores - Total Received"], className="subtitle padded"
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
                                # style=dict(paddingRight=50)
                            ),
                            html.Div( # COL ORDER STATUS
                                [
                                    html.Div(
                                        [
                                            html.H4(
                                                ["Customer Satisfaction over Time"], className="subtitle padded"
                                            ),
                                        ],className='Row'
                                    ),
                                    
                                    html.Div( #Col1
                                        [
                                            dcc.Graph(
                                                figure=month_satisf(),
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        # className="nine columns",
                                    
                    
                                    ),
                                ],
                                className="six columns",
                                # style=dict(paddingLeft=50)
                            ),
                            
                        ], className='row'
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H4(
                                        [
                                            'Review Score vs Delivery Wait Time'
                                        ],
                                        className="subtitle padded"
                                    ),
                                    dcc.Graph(
                                        figure=delay_wait(),
                                        config={"displayModeBar": False},
                                    ),
                                ], className='row'
                            ),
                            html.Div([
                                    dcc.Markdown(
                                        '''
                                        **Wait Time:** time between purchase and delivery date (in days).  
                                          
                                        **Delay vs Expected:** The difference between the estimated delivery and actual delivery date.
                                        '''),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Div([
                                        dcc.Markdown(
                                            f'''
                                            ###### There are two periods with longer wait times:
                                            End of November / Beginning of December 2017  
                                            End of February / Beginning of March 2017  
                                               
                                            ---
                                            '''),
                                        dcc.Markdown(
                                            f"Wait time mean: {round(wait_time_mean(), 2)} days"
                                        ),
                                        dcc.Markdown(
                                            f"Delay vs Expected Time mean: {round(delay_vs_expected_mean(),2)} days"
                                        )
                                        
                                    ],
                                    className="product2",
                                    ),
                                    html.Br(),
                                ],
                                className='row'
                            ),
                        
                        ],
                        
                    ),
                    
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
