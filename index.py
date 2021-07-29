import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from utils import Header

from pages import (
    overview,
    reviewsModel1,
)


app.layout = html.Div(
    [
        html.Div(
            [
                Header(app),
                html.Div(id='page-content', children=[])
            ],className="page",
        ),
    ]
)

# Update page - Tabs
@app.callback(Output('page-content', 'children'),[Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-0':
        return overview.layout
    elif tab == 'tab-1':
        return reviewsModel1.layout
    else:
        return overview.layout



if __name__ == '__main__':
    app.run_server(debug=True)
