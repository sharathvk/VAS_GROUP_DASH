from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

from multiapps.apps import dashboard, sales, purchase

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.layout = dbc.Container(
    [
        dcc.Location(id="url"),

        dbc.NavbarSimple(
            brand="Sales & Purchase System",
            color="dark",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
                dbc.NavItem(dbc.NavLink("Sales", href="/sales")),
                dbc.NavItem(dbc.NavLink("Purchase", href="/purchase")),
            ]
        ),

        html.Div(id="page-content", className="mt-4")
    ],
    fluid=True
)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def route_pages(pathname):
    if pathname == "/sales":
        return sales.layout
    elif pathname == "/purchase":
        return purchase.layout
    else:
        return dashboard.layout


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8050)


