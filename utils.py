import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("antonio_green.svg"),
                                className="logo",
                            ),

                        ],
                        className='eleven columns'
                    ),
                    
                    html.Div(
                        [
                            html.A(
                                html.Button("GitHub Repo", id="learn-more-button"),
                                href="https://github.com/antoniovmonge/olist-dash",
                            ),
                            html.A(
                                html.Button("Portfolio",id="learn-more-button-2"),
                                href="https://antonio-vm-portfolio.herokuapp.com/",
                            ),
                        ],
                        className='one column',
                        style=dict(textAlign='right')
                    ),                 
                ],
                className="row",
            ),
            html.Div(
                [
                    # html.Div(
                    #     [
                            
                    #         html.H5('🚧(Project Under Construction)'),
                        
                    #     ],
                    #     className="twelve columns",
                    #     style=dict(textAlign='center')
                    # ),
                    
                    html.Div(
                        [
                            
                            html.H5("E-Commerce Analysis")
                        ],
                        className="seven columns main-title",
                    ),
                    # html.Div(
                    #     [
                    #         dcc.Link(
                    #             "Full View",
                    #             href="/olist-financial-report/full-view",
                    #             className="full-view-link",
                    #         )
                    #     ],
                    #     className="five columns",
                    # ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


# def get_menu():
#     menu = html.Div(
#         [
#             dcc.Link(
#                 "Overview",
#                 href="/olist-financial-report/overview",
#                 className="tab first",
#             ),
#             dcc.Link(
#                 "Reviews Model 1",
#                 href="/olist-financial-report/reviews-model-1",
#                 className="tab",
#             ),
#             # dcc.Link(
#             #     "Portfolio & Management",
#             #     href="/olist-financial-report/portfolio-management",
#             #     className="tab",
#             # ),
#             # dcc.Link(
#             #     "Fees & Minimums", href="/olist-financial-report/fees", className="tab"
#             # ),
#             # dcc.Link(
#             #     "Distributions",
#             #     href="/olist-financial-report/distributions",
#             #     className="tab",
#             # ),
#             # dcc.Link(
#             #     "News & Reviews",
#             #     href="/olist-financial-report/news-and-reviews",
#             #     className="tab",
#             # ),
#         ],
#         className="row all-tabs",
#     )
#     return menu

def get_menu():
    menu = html.Div(
        [
            dcc.Tabs(
                id='tabs',
                    value='Tab One',
                    parent_className='custom-tabs',
                    # className='custom-tabs-container',
                    children=[
                        dcc.Tab(
                            label='Overview',
                            value='tab-0',
                            # className='custom-tab',
                            # selected_className='custom-tab--selected'
                        ),
                        dcc.Tab(
                            label='Reviews-Analysis Model 1',
                            value='tab-1',
                            # className='custom-tab',
                            # selected_className='custom-tab--selected'
                        ),
                    ]
            )
        ],
        # className="row all-tabs",
    )
    
    return menu

# def make_dash_table(df):
#     """ Return a dash definition of an HTML table for a Pandas dataframe """
#     table = []
#     for index, row in df.iterrows():
#         html_row = []
#         for i in range(len(row)):
#             html_row.append(html.Td([row[i]]))
#         table.append(html.Tr(html_row))
#     return table
