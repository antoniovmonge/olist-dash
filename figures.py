import plotly.graph_objs as go
import plotly.express as px

import pandas as pd

# get the data
from olistdash.data import Olist
data = Olist().get_data()

df = data['order_payments'][['order_id','payment_value']].merge(data['orders'][['order_id','order_purchase_timestamp']], on='order_id', how='outer')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df = df.set_index('order_purchase_timestamp').sort_index()
df_daily = pd.DataFrame(df.resample('D')['payment_value'].sum()).reset_index()
df_daily = df_daily[df_daily['order_purchase_timestamp'] <= '2018-07-31']

def fig1():
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
    return fig

def review_score():
    fig = go.Figure(
        data=[go.Bar(x=data['order_reviews']['review_score'])])
    return fig
