import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

# get the data
# from olistdash.data import Olist
# data = Olist().get_data()

# df = data['order_payments'][['order_id','payment_value']].merge(data['orders'][['order_id','order_purchase_timestamp']], on='order_id', how='outer')
# df = pd.read_csv('s3://olistdashdb/csv/df.csv')
df = pd.read_csv('raw_data/csv/df.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
# df = df[(df['order_purchase_timestamp'] >= '2017-01-01') & (df['order_purchase_timestamp'] <= '2018-07-31' )]
df = df[(df['order_purchase_timestamp'] >= '2017-01-01')]

df = df.set_index('order_purchase_timestamp').sort_index()

df_daily = pd.DataFrame(df.resample('D')['payment_value'].sum()).reset_index()

df_monthly = pd.DataFrame(df.resample('M')['payment_value'].sum()).reset_index()


# reviews = data['order_reviews'].copy()
reviews = pd.read_csv('s3://olistdashdb/csv/reviews.csv')
# handle datetime
reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
reviews.set_index('review_creation_date', inplace=True)

# orders = data['orders'].copy()

# orders = pd.read_csv('s3://olistdashdb/csv/orders.csv')
orders=pd.read_csv('raw_data/csv/orders.csv')
orders = orders.query("order_status=='delivered'").reset_index()
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
# orders = orders[(orders['order_purchase_timestamp'] >= '2017-01-01') & (orders['order_purchase_timestamp'] <= '2018-07-31' )]
orders = orders[(orders['order_purchase_timestamp'] >= '2017-01-01')]
orders['delay_vs_expected'] = (orders['order_estimated_delivery_date'] - orders['order_delivered_customer_date']) / np.timedelta64(24, 'h')
def handle_delay(x):
    if x < 0:
        return abs(x)
    else:
        return 0
    
orders.loc[:,'delay_vs_expected'] = orders['delay_vs_expected'].apply(handle_delay)
orders['wait_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')




def fig1():
    fig = go.Figure(
        [
            go.Scatter(
                x=df_daily["order_purchase_timestamp"],
                y=df_daily["payment_value"],
                line=dict(color = "#DE3562"),
                name="Daily Payments",
            )
        ]
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=df_monthly["order_purchase_timestamp"],
    #         y=df_monthly["payment_value"],
    #         line={"color": "#35CDDE"},
    #         name="Monthly payment value"
    #     )
    # )
    fig.update_layout(
        title=dict(
            text="Daily revenue",
            y=1,
            x=0.5,
            xanchor= 'center',
            yanchor= 'top'
        ),
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
            y=0.98,
            xanchor="center",
            x=0.12,
            font=dict(
                size=10,
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
                ],
                'x': 1,
                'xanchor':'right',
                'y':1.1,
                'yanchor':'top',
            },
            'rangeslider':{'visible': True},
            "showline": True,
            "type": "date",
            "zeroline": False,
        },
        yaxis={
            # "autorange": True,
            "range": [
                0,
                80000,
            ],
            "showline": True,
            "type": "linear",
            "zeroline": False,
        },
    )
    fig.update_yaxes(ticksuffix=" BRL")
    return fig

def payments_month():
    fig = go.Figure(
        [
            go.Bar(
                name="Payments Monthly Value",
                x=df_monthly["order_purchase_timestamp"],
                y=df_monthly["payment_value"],
                xperiod="M1",
                xperiodalignment="middle",
            )
        ]
    )
    fig.update_traces(marker_color='rgb(158,202,225)')
    fig.add_trace(
        go.Scatter(
                x=df_daily["order_purchase_timestamp"],
                y=df_daily["payment_value"],
                line=dict(color = "#DE3562"),
                name="Daily Payments",
            )
    )
    # fig.add_trace(
    #     go.Bar(
    #         name="Payments Monthly Value",
    #         x=df_monthly["order_purchase_timestamp"],
    #         y=df_monthly["payment_value"],
    #         xperiod="M1",
    #         xperiodalignment="middle",
    #     )
    # )
    fig.update_layout(
        
        title=dict(
            text="Monthly Revenue",
            y=1,
            x=0.5,
            xanchor= 'center',
            yanchor= 'top'
        ),
        autosize=True,
    #                 width=700,
    #                 height=200,
    #                 font=dict(
    #                     family="Lato, Sans-Serif",
    #                     size= 10
    #                     ),
        showlegend = True,
        # hovermode  = 'x',
        margin={
            "r": 30,
            "t": 30,
            "b": 30,
            "l": 30,
        },
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="center",
            x=0.16,
            font=dict(
                size=10,
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
                ],
                'x': 1,
                'xanchor':'right',
                'y':1.1,
                'yanchor':'top',

            },
            'rangeslider':{'visible': True},
            "showline": True,
            "type": "date",
            "zeroline": False,
        },
        yaxis={
            "autorange": True,
            # "range": [
            #     0,
            #     80000,
            # ],
            "showline": True,
            "type": "linear",
            "zeroline": False,
        },
    )
    fig.update_yaxes(ticksuffix=" BRL")
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        showgrid=True,
        ticklabelmode="period"
    )

    return fig

def review_score():
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=reviews['review_score'].value_counts().reset_index()['index'],
            y=reviews['review_score'].value_counts().reset_index()['review_score'],
            marker_color='#157E98'
        )
    )
    fig.update_layout(
        title_text="Review Score Count (Valid Reviews)",
        title_font_size=15,
        # margin={
        #     "r": 30,
        #     "t": 30,
        #     "b": 30,
        #     "l": 30,
        # },
        )
    fig.update_xaxes(title_text= 'review score')
    fig.update_yaxes(title_text= 'count')
    return fig

def table_review_score():
    return reviews['review_score'].value_counts().reset_index().sort_values(by='index',axis=0,ascending=False)

def order_status():
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=orders['order_status'].value_counts().reset_index()['index'],
            y=orders['order_status'].value_counts().reset_index()['order_status'],
            marker_color='#157E98',
            # orientation='h'
        )
    )
    # fig.update_layout(
    #     title_text="Order Status",
    #     title_font_size=20,
    # )
    # fig.update_xaxes(title_text= 'Order Status')
    # fig.update_yaxes(title_text= 'count')
    return fig

def table_order_status():
    return orders['order_status'].value_counts().reset_index()

def month_satisf():
    
    fig = go.Figure(
    [
        go.Scatter(
            x=reviews.loc['2017-02-01':].resample('M').agg({'review_score':'mean'}).reset_index()['review_creation_date'],
            y=reviews.loc['2017-02-01':].resample('M').agg({'review_score':'mean'}).reset_index()['review_score'],
            line=dict(color = "#DE3562"),
            name="mean review score",
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
        title="Mean review_score - monthly customer satisfaction",
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
        # legend=dict(
        #     yanchor="bottom",
        #     y=0.05,
        #     xanchor="left",
        #     x=0.01,
        #     font=dict(
        #         size=10,
        #     ),
        #     bgcolor="rgba(255, 255, 255, 0.8)",
        # ),
    #                 titlefont=dict(
    #                     family="Lato, Sans-Serif",
    #                     size= 10
    #                     ),
        xaxis={
            "autorange": True,
        },
        yaxis={
            "autorange": True,
            # "range": [
            #     1,
            #     5,
            # ],
            "showline": True,
            "type": "linear",
            "zeroline": False,
        },
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period"

    )
    fig.update_yaxes(ticksuffix=" ⭐ ")
    return fig
    
def delay_wait():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
            go.Scatter(
                x=reviews.loc['2017-02-01':].resample('W').agg({'review_score':'mean'}).reset_index()['review_creation_date'],
                y=reviews.loc['2017-02-01':].resample('W').agg({'review_score':'mean'}).reset_index()['review_score'],
                line=dict(color = "#DE3562"),
                name="REVIEW SCORE (Weekly Mean)",
            ),
            secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(
            x=orders.set_index('order_purchase_timestamp').resample('W')[['delay_vs_expected', 'wait_time']].mean().reset_index()['order_purchase_timestamp'],
            y=orders.set_index('order_purchase_timestamp').resample('W')[['delay_vs_expected', 'wait_time']].mean().reset_index()['wait_time'],
            line={"color": "green"},
            name="Wait Time",
            
        ),
        secondary_y=False,    
    )
    fig.add_trace(
        go.Scatter(
                x=orders.set_index('order_purchase_timestamp').resample('W')[['delay_vs_expected', 'wait_time']].mean().reset_index()['order_purchase_timestamp'],
                y=orders.set_index('order_purchase_timestamp').resample('W')[['delay_vs_expected', 'wait_time']].mean().reset_index()['delay_vs_expected'],
                line=dict(color = "blue"),
                name="Delay vs Expected",
            ),
            secondary_y=False,
    )
    fig.update_layout(
        title=dict(
            text="Customer Wait Time",
            # y=1,
            # x=0.5,
            # xanchor= 'center',
            # yanchor= 'top'
        ),
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
        # legend=dict(
        #     yanchor="bottom",
        #     y=0.01,
        #     xanchor="left",
        #     x=0.01,
        #     font=dict(
        #         size=10,
        #     ),
        #     bgcolor="rgba(255, 255, 255, 0.6)",
        # ),
                    # titlefont=dict(
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
                ],
                'x': 0.945,
                'xanchor':'right',
                'y':1.1,
                'yanchor':'top',
            },
            'rangeslider':{'visible': True},
            "showline": True,
            "type": "date",
            "zeroline": False,
        },
        yaxis={
            # "autorange": True,
            "range": [
                0,
                40,
            ],
            "showline": True,
            "type": "linear",
            "zeroline": False,
        },
    )
    fig.update_yaxes(title_text="Delay Time", secondary_y=False)
    fig.update_yaxes(
        title_text="Review Score",
        secondary_y=True,
        tickprefix=" ⭐ "
        )
    # fig.update_yaxes(ticksuffix=" BRL")
    return fig

def wait_time_mean():
    return orders['wait_time'].mean()

def delay_vs_expected_mean():
    return orders['delay_vs_expected'].mean()