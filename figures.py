import plotly.graph_objs as go
import plotly.express as px

import pandas as pd

# get the data
from olistdash.data import Olist
data = Olist().get_data()

df = data['order_payments'][['order_id','payment_value']].merge(data['orders'][['order_id','order_purchase_timestamp']], on='order_id', how='outer')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df = df[(df['order_purchase_timestamp'] >= '2017-01-01') & (df['order_purchase_timestamp'] <= '2018-07-31' )]
df = df.set_index('order_purchase_timestamp').sort_index()

df_daily = pd.DataFrame(df.resample('D')['payment_value'].sum()).reset_index()


df_monthly = pd.DataFrame(df.resample('M')['payment_value'].sum()).reset_index()


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
            x=0.15,
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
                ]
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
        updatemenus=[
            dict(
                
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.11,
                xanchor="left",
                y=1.1,
                yanchor="top"
            )
        ],
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
            y=0.9,
            xanchor="center",
            x=0.15,
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
            x=data['order_reviews']['review_score'].value_counts().reset_index()['index'],
            y=data['order_reviews']['review_score'].value_counts().reset_index()['review_score'],
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
    return data['order_reviews']['review_score'].value_counts().reset_index().sort_values(by='index',axis=0,ascending=False)

def order_status():
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data['orders']['order_status'].value_counts().reset_index()['index'],
            y=data['orders']['order_status'].value_counts().reset_index()['order_status'],
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
    return data['orders']['order_status'].value_counts().reset_index()

def month_satisf():
    reviews = data['order_reviews'].copy()
    # handle datetime
    reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
    reviews.set_index('review_creation_date', inplace=True)
    fig = go.Figure(
    [
        go.Scatter(
            x=reviews.loc['2017-02-01':].resample('M').agg({'review_score':'mean'}).reset_index()['review_creation_date'],
            y=reviews.loc['2017-02-01':].resample('M').agg({'review_score':'mean'}).reset_index()['review_score'],
            line=dict(color = "#DE3562"),
            name="review score",
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
        title="Ploting monthly customer satisfaction, as mean review_score",
        autosize=True,
    #                 width=700,
    #                 height=200,
    #                 font=dict(
    #                     family="Lato, Sans-Serif",
    #                     size= 10
    #                     ),
        showlegend = True,
        hovermode  = 'x',
        # margin={
        #     "r": 30,
        #     "t": 30,
        #     "b": 30,
        #     "l": 30,
        # },
        # legend=dict(
        #         yanchor="top",
        #         y=0.9,
        #         xanchor="center",
        #         x=0.05,
        #         font=dict(
        #             size=12,
        #         )
        #     ),
    #                 titlefont=dict(
    #                     family="Lato, Sans-Serif",
    #                     size= 10
    #                     ),
        xaxis={
            "autorange": True,
        },
        yaxis={
            # "autorange": True,
            "range": [
                1,
                5,
            ],
            "showline": True,
            "type": "linear",
            "zeroline": False,
        },
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y"
    )
    return fig
    