# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import (
    overview,
    reviewsModel1,
    # portfolioManagement,
    # feesMins,
    # distributions,
    # newsReviews,
)

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name":"viewport","content":"width=device-width"},
        {"name": "title", "content":"E-Commerce Data Analysis"},
        {"name":"description", "content":"Interactive Dashboard Application - Work in Progress"},
        {"property": "og:type", "content": "website"},
        {"property": "og:url", "content": "https://olist-dash-antonio.herokuapp.com/"},
        {"property": "og:title", "content": "E-Commerce Data Analysis"},
        {"property": "og:description", "content": "Interactive Dashboard Application - Work in Progress"},
        {"property": "og:image", "content": "assets/financial-analysis-big.svg"},
        {"property": "twitter:card", "content": "summary_large_image"},
        {"property": "twitter:url ", "content": "https://olist-dash-antonio.herokuapp.com/"},
        {"property": "twitter:title", "content": "E-Commerce Data Analysis"},
        {"property": "twitter:description", "content": "Interactive Dashboard Application - Work in Progress"},
        {"property": "twitter:image", "content": "assets/financial-analysis-big.svg"}
    ],
)
app.title = "E-Commerce Analysis"

server = app.server



# Describe the layout/ UI of the app
# app.layout = html.Div(
#     [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
# )




# Update page
# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def display_page(pathname):
#     if pathname == "/olist-financial-report/reviews-model-1":
#         return reviewsModel1.create_layout(app)
#     # elif pathname == "/olist-financial-report/portfolio-management":
#     #     return portfolioManagement.create_layout(app)
#     # elif pathname == "/olist-financial-report/fees":
#     #     return feesMins.create_layout(app)
#     # elif pathname == "/olist-financial-report/distributions":
#     #     return distributions.create_layout(app)
#     # elif pathname == "/olist-financial-report/news-and-reviews":
#     #     return newsReviews.create_layout(app)
#     elif pathname == "/olist-financial-report/full-view":
#         return (
#             overview.create_layout(app),
#             reviewsModel1.create_layout(app),
#             # portfolioManagement.create_layout(app),
#             # feesMins.create_layout(app),
#             # distributions.create_layout(app),
#             # newsReviews.create_layout(app),
#         )
#     else:
#         return overview.create_layout(app)


# if __name__ == "__main__":
#     app.run_server(debug=True)
