from dash import html, Input, Output, State
import dash_bootstrap_components as dbc
from dash import callback

layout = dbc.Container(
    [
        html.H3("Sales Entry", className="text-center mb-4"),

        dbc.Input(id="s_phno", placeholder="Phone Number", className="mb-3"),
        dbc.Input(id="s_vehicle", placeholder="Vehicle Number", className="mb-3"),
        dbc.Input(id="s_item", placeholder="Item Name", className="mb-3"),

        dbc.Row(
            [
                dbc.Col(dbc.Input(id="s_price", type="number", placeholder="Price"), md=6),
                dbc.Col(dbc.Input(id="s_qty", type="number", placeholder="Quantity"), md=6),
            ],
            className="mb-3"
        ),

        dbc.Button("Save Sale", id="save_sale", color="success", className="w-100"),
        html.Br(), html.Br(),

        dbc.Alert(id="sale_output", is_open=False)
    ],
    # md=6
)


@callback(
    Output("sale_output", "children"),
    Output("sale_output", "is_open"),
    Input("save_sale", "n_clicks"),
    State("s_phno", "value"),
    State("s_vehicle", "value"),
    State("s_item", "value"),
    State("s_price", "value"),
    State("s_qty", "value"),
)
def save_sale(n, phno, vehicle, item, price, qty):
    if not n:
        return "", False

    if not all([phno, vehicle, item, price, qty]):
        return "❌ Please fill all sales fields", True

    total = price * qty
    return f"✅ Sale Saved | Total = ₹{total}", True
