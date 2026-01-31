from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        html.H3("Dashboard", className="text-center mb-4"),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Total Sales"),
                                html.H3("₹ 0")
                            ]
                        ),
                        color="success",
                        inverse=True
                    ),
                    md=6
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Total Purchases"),
                                html.H3("₹ 0")
                            ]
                        ),
                        color="primary",
                        inverse=True
                    ),
                    # md=6
                ),
            ]
        )
    ]
)
