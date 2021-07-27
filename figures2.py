import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

import statsmodels.formula.api as smf

#get the orders data
from olistdash.order import Order
orders = Order().get_training_data(with_distance_seller_customer=True)

features = [
    "wait_time",
    "delay_vs_expected",
    "number_of_products",
    "number_of_sellers",
    "price",
    "freight_value",
    "distance_seller_customer",
]
orders_standardized = orders.copy()
for f in features:
    mu = orders[f].mean()
    sigma = orders[f].std()
    orders_standardized[f] = orders[f].map(lambda x: (x - mu) / sigma)
formula = "review_score ~ " + ' + '.join(features)
model4 = smf.ols(formula=formula, data=orders_standardized).fit()
model_df = pd.DataFrame(model4.params[1:].sort_values()).reset_index()
model_df.columns = ['features', 'correlation']
model_df


def heatmap1():
    # fig = go.Heatmap(orders.corr())
    #     )
    # )
    fig = px.imshow(
        orders.corr(),
        # template='simple_white',
    )
    return fig

def model_summary_tab_0():
    return pd.read_html(
        model4.summary().tables[0].as_html(),
        header=0,
        index_col=0
        )[0].reset_index()

def model_summary_tab_1():
    return pd.read_html(
        model4.summary().tables[1].as_html(),
        header=0,
        index_col=0
        )[0].reset_index()[1:]

def model_summary_tab_2():
    return pd.read_html(
        model4.summary().tables[2].as_html(),
        header=0,
        index_col=0
        )[0].reset_index()

def correlation_bars():
    fig = px.bar(
        model_df,
        y='features',
        x='correlation',
        orientation='h',
        # template='simple_white'
        )
    return fig


