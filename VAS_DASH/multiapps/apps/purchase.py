from dash import html, Input, Output, State
import dash_bootstrap_components as dbc
from dash import callback

layout = dbc.Container(
    [
        html.H3("Purchase Entry", className="text-center mb-4"),

        dbc.Input(id="p_vendor", placeholder="Vendor Name", className="mb-3"),
        dbc.Input(id="p_item", placeholder="Item Name", className="mb-3"),

        dbc.Row(
            [
                dbc.Col(dbc.Input(id="p_price", type="number", placeholder="Price"), md=6),
                dbc.Col(dbc.Input(id="p_qty", type="number", placeholder="Quantity"), md=6),
            ],
            className="mb-3"
        ),

        dbc.Button("Save Purchase", id="save_purchase", color="primary", className="w-100"),
        html.Br(), html.Br(),

        dbc.Alert(id="purchase_output", is_open=False)
    ],
    # md=6
)


@callback(
    Output("purchase_output", "children"),
    Output("purchase_output", "is_open"),
    Input("save_purchase", "n_clicks"),
    State("p_vendor", "value"),
    State("p_item", "value"),
    State("p_price", "value"),
    State("p_qty", "value"),
)
def save_purchase(n, vendor, item, price, qty):
    if not n:
        return "", False

    if not all([vendor, item, price, qty]):
        return "❌ Please fill all purchase fields", True

    total = price * qty
    return f"✅ Purchase Saved | Total = ₹{total}", True
