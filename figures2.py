import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

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

predicted_review_score = model4.predict(orders_standardized[features])
residuals = predicted_review_score - orders_standardized.review_score

def heatmap1():
    # fig = go.Heatmap(orders.corr())
    #     )
    # )
    fig = px.imshow(
        orders.corr(),
        # template='simple_white',
    )
    return fig

def correlation_bars():
    fig = px.bar(
        model_df,
        y='features',
        x='correlation',
        orientation='h',
        # template='simple_white'
        )
    fig.update_layout(
        margin={
            "r": 20,
            "t": 30,
            "b": 60,
            "l": 30,
        },
        height=300
    )
    fig.update_traces(
        width=0.4,
        # marker_line=dict(width=3)
    )
    fig.update_yaxes(title=None)
    
    return fig

# TABLES STATSMODEL
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
        )[0].reset_index()

def model_summary_tab_2():
    return pd.read_html(
        model4.summary().tables[2].as_html(),
        header=0,
        index_col=0
        )[0].reset_index()

# PERFORMANCE
def residuals_mean():
    return residuals.mean()

def rmse_function():
    return (residuals.map(lambda x: x**2).sum() / len(residuals))**0.5

def model_performance():
    fig = ff.create_distplot(
        [residuals],
        group_labels=['distplot'],
        bin_size=.2,
        show_rug=False,
        histnorm='probability',
    )
    fig.update_layout(
        showlegend=False,
        title='Residuals Density Plot',
        # margin={
        #     # "r": 30,
        #     "t": 30,
        #     # "b": 30,
        #     "l": 30,
        # }
    )
    fig.update_yaxes(
        title='Density'
    )
    return fig

def predicted_vs_actual():
    group_labels=['predicted value','real value']
    colors = ['rgb(0, 0, 100)', "#DE3562"]
    # Create distplot with custom bin_size
    fig = ff.create_distplot(
        [
            predicted_review_score,
            orders.review_score
        ],
        group_labels,
        show_hist=False,
        bin_size=.2,
        show_rug=False,
        colors=colors,
        histnorm='probability',
    )
    fig.update_layout(
        xaxis={
        # "autorange": True,
            "range": [
                "1",
                "5",
            ],
        }
    )
    return fig