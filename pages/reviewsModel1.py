import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header
import pandas as pd
# import pathlib
import dash_table

from figures2 import *

# get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../data").resolve()


layout = html.Div(
        [
            # Header(app),
            # page 2
            html.Div(
                [
                    # Row
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(
                                        ["Review Score Correlation"], className="subtitle padded"
                                    ),
                                    dcc.Markdown('Inspecting the varius correlations between features. Looking for the ones related with `review_score`'),
                                    dcc.Graph(
                                        figure=heatmap1(),
                                        config={"displayModeBar": False}
                                    ),
                                    dcc.Markdown(
                                        '''
                                        - `wait_time` is the more correlated feature `review_score`.
                                        Negative Correlation (Bigger wait time less Sore in review).
                                        The second feature with bigger correlation (also negative) is `delay_vs_spected`. However, these two features are also highly correlated with each other. 
                                        - Using `statsmodels` to distinguish the effect of one feature, **holding the other one constant**.
                                        '''
                                        )
                                    # html.Table(make_dash_table(df_current_prices)),

                                ],
                                className="six columns",
                                style=dict(paddingRight=50),
                            ),
                            
                            html.Div(
                                [
                                    html.H5(
                                        ["Data Frame"],
                                        className="subtitle padded",
                                    ),
                                    html.Br(),
                                    dcc.Markdown(
                                        '''
                                        
                                        - `order_id` (_str) the id of the order_
                                        - `wait_time` (_float) the number of days between order_date and delivered_date_
                                        - `expected_wait_time` (_float) the number of days between order_date and estimated_delivery_date_
                                        - `delay_vs_expected` (_float) if the actual delivery date is later than the estimated delivery date, returns the absolute number of days between the two dates, otherwise return 0_
                                        - `order_status` (_str) the status of the order_
                                        - `dim_is_five_star` (_int) 1 if the order received a five_star, 0 otherwise_
                                        - `dim_is_one_star` (_int) 1 if the order received a one_star, 0 otherwise_
                                        - `review_score`(_int) from 1 to 5_
                                        - `number_of_product` (_int) number of products that the order contains_
                                        - `number_of_sellers` (_int) number of sellers involved in the order_
                                        - `price` (_float) total price of the order paid by customer_
                                        - `freight_value` (_float) value of the freight paid by customer_
                                        - `distance_customer_seller` (_float) the distance in km between customer and seller_
                                        '''
                                    ),
                                ],
                                className="six columns",
                                style=dict(paddingLeft=50),
                            ),
                        ],
                        className="row ",
                    ),
                    html.Div(
                        [
                            dcc.Markdown('---')
                        ],className='row'
                    ),
                    html.Div( # ROW 2
                        [
                            html.Div(
                                [
                                    html.H5("MULTIVARIATE REGRESSION", className="subtitle padded"),
                                    # html.Br(),
                                    dcc.Markdown(
                                        '''
                                        Search of the feature with the greatest influence for a low `review_score`.
                                          
                                        Running an OLS (Ordinary Least Squares) model to analyse the impact of variations on the selected features
                                        (independent variables), on the the target: `review_score` (dependent variable).
                                        The multivariate regression allows us to isolate the impact of one feature,
                                        while controlling the effect of other features. These new coefficients
                                        are called partial correlation coefficients.
                                          
                                        The multivariate regression allows us to isolate the impact of one feature,
                                        while controlling the effect of other features. These new coefficients are called
                                        partial correlation coefficients.
                                          
                                        '''
                                    ),
                                    dcc.Graph(
                                        figure=correlation_bars(),
                                        config={"displayModeBar": False}
                                    ),
                                    
                                    dcc.Markdown(
                                        '''
                                        - `wait_time` is the biggest explanatory variable
                                        - The more `products` and `sellers` there are for a single order,
                                        the lower the `review_score`. 
                                        - Distance also plays a role.a
                                            
                                        - Overall, this multivariate regression remains statistically significant,
                                        because its F-statistics are much greater than 1 (at least one feature has a
                                        very low p-value)

                                        - R-squared hasn't increased by much. Most of the explanability of review_score
                                        lies outside of the orders dataset.

                                        Low R-squared is common when the number of observations (n) is much higher than
                                        the number of features (p). Relevant insights can still be derived from such regressions,
                                        provided they are statistically significant.
                                        '''
                                    ),
                                ],
                                style=dict(paddingRight=50),
                                className="six columns",
                            ),
                            # html.Div(
                            #     [
                            #         html.Br()
                            #     ], className='one column'
                            #     ),
                            html.Div(
                                [
                                    html.H5("OLS Regression Results", className="subtitle padded"),
                                    # html.P(
                                    #     'OLS Regression Results',
                                    #     style=dict(
                                    #         textAlign='center',
                                    #         fontFamily='Courier',
                                    #         fontSize=20,
                                    #         fontWeight='bold'
                                    #         )
                                    # ),
                                    html.Br(),
                                    html.Div(
                                        [
                                            dash_table.DataTable(
                                                columns=[{"name": i, "id": i} for i in model_summary_tab_0().columns],
                                                data=model_summary_tab_0().to_dict('records'),
                                                style_as_list_view=True,
                                                style_header={
                                                    'backgroundColor': 'white',
                                                    # 'fontWeight': 'bold'
                                                },
                                                style_cell = {
                                                    # 'border': 'none',
                                                    }
                                            ),
                                            html.Br(),
                                            dash_table.DataTable(
                                                columns=[
                                                    {
                                                        'name':'','id':'index'
                                                    },
                                                    {
                                                        'name':'coef','id':'coef'
                                                    },
                                                    {
                                                        'name':'std err','id':'std err'
                                                    },
                                                    {
                                                        'name':'t','id':'t'
                                                    },
                                                    {
                                                        'name':'P>|t|','id':'P>|t|'
                                                    },
                                                    {
                                                        'name':'[0.025','id':'[0.025'
                                                    },
                                                    {
                                                        'name':'0.975]','id':'0.975]'
                                                    },
                                
                                                ],
                                                # columns=[{"name": i, "id": i} for i in model_summary_tab_1().columns],
                                                data=model_summary_tab_1().to_dict('records'),
                                                style_as_list_view=True,
                                                style_header={
                                                    'backgroundColor': 'white',
                                                    'fontWeight': 'bold'
                                                },
                                            ),
                                            html.Br(),
                                            dash_table.DataTable(
                                                columns=[{"name": i, "id": i} for i in model_summary_tab_2().columns],
                                                data=model_summary_tab_2().to_dict('records'),
                                                style_as_list_view=True,
                                                style_header={
                                                    'backgroundColor': 'white',
                                                    # 'fontWeight': 'bold'
                                                },
                                                # style_cell = {'border': 'none'}
                                            ),
                                        ]
                                    ),  
                                ],
                                style=dict(paddingLeft=50),
                                className="six columns",
                            )
                        ],
                        className="row ",
                    ),
                    html.Div(
                        [
                            dcc.Markdown('---')
                        ],className='row'
                    ),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(
                                        [
                                            "OLS-Model Performance Check"
                                        ],
                                        className="subtitle padded",
                                    ),
                                    dcc.Markdown(
                                        '''
                                        Regression performance should not be measured only by it's R-squared.
                                        It is always important to visualize the distribution of the predictions, and especially the residuals.
                                        '''
                                    ),
                                    dcc.Graph(
                                        figure=performance_card(),
                                        config={'displayModeBar': False}
                                    ),
                                    dcc.Markdown(f' - Computed residuals. **Residuals mean: {round(residuals_mean(),8)}**'),
                                    # dcc.Markdown(
                                    #     [
                                    #     f'###### '
                                    #     ],
                                    #     style=dict(
                                    #         textAlign='center',
                                    #         fontWeight='bold'
                                    #     )
                                    # ),
                                    html.Div(
                                        [
                                            dcc.Markdown(
                                                '*Their mean is equal to 0 (always the case in linear regression)',
                                                style=dict(
                                                    fontSize=12,
                                                    color='rgb(145,145,145)',
                                                    textAlign='center',
                                                    
                                                )
                                            ),

                                        ],
                                        style=dict(
                                            # marginLeft=60,
                                            marginTop=15
                                        )
                                    ),
                                    dcc.Markdown(
                                        f'''
                                        - Computed associated RMSE. **RMSE: {rmse_function()}**
                                        '''
                                    ),
                                    
                                    dcc.Markdown(
                                        [
                                        f'###### '
                                        ],
                                        style=dict(
                                            textAlign='center',
                
                                        )
                                    ),
                                    dcc.Markdown(
                                        '''
                                        ###### Histogram of `residuals`.
                                        '''
                                    ),
                                    dcc.Graph(
                                        
                                            figure=model_performance(),
                                            config={"displayModeBar": False}
                                        
                                    ),
    
                                ],
                                style=dict(paddingRight=50),
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H5(
                                        [
                                            "OLS Model Prediction vs Real"
                                        ],
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        
                                            figure=predicted_vs_actual(),
                                            config={"displayModeBar": False}
                                        
                                    ),
                                    dcc.Markdown(
                                        '''
                                        ###### **Analysis:**
                                        ⚠ This model is **not** performing good, for two reasons:
                                        1. First, because it doesn't have enough features to explain a significant proportion of the review_scores (low R-squared)
                                        2. Secondly, because it is done by trying to fit a "linear regression" function to a discreet classification problem.
                                        '''
                                    )
                                ],
                                className="six columns",
                                style=dict(paddingLeft=50),
                            )
                        ],
                        className="row ",
                    ),
                    
                ],
                className="sub_page",
            ),
        ],
        # className="page",
    )
