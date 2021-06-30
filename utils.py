import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("antonio_logo_SVG_3.svg"),
                        className="logo",
                    ),
                    html.A(
                        html.Button("Notion Portfolio", id="learn-more-button"),
                        href="https://www.notion.so/Antonio-VM-Data-Analyst-Portfolio-b1d15564f6cb470a8e3ad83f2a91ca16",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Olist Financial Analytics")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/olist-financial-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/olist-financial-report/overview",
                className="tab first",
            ),
            dcc.Link(
                "Price Performance",
                href="/olist-financial-report/price-performance",
                className="tab",
            ),
            dcc.Link(
                "Portfolio & Management",
                href="/olist-financial-report/portfolio-management",
                className="tab",
            ),
            dcc.Link(
                "Fees & Minimums", href="/olist-financial-report/fees", className="tab"
            ),
            dcc.Link(
                "Distributions",
                href="/olist-financial-report/distributions",
                className="tab",
            ),
            dcc.Link(
                "News & Reviews",
                href="/olist-financial-report/news-and-reviews",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
