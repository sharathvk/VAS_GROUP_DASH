from dash import html, Input, Output, State, callback, callback_context
import dash_bootstrap_components as dbc
from datetime import date
from multiapps.utils.validations import validate_mobile_number, validate_vehicle_number

form_content = [
    html.H3("Purchase Entry", className="text-center mb-4"),

    # ---- Row 1 ----
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Date"),
                    dbc.Input(type="date", id="p_date", value=str(date.today())),
                ],
                md=6
            ),
            dbc.Col(
                [
                    dbc.Label("Vendor Name "),
                    dbc.Input(id="p_vendor"),
                ],
                md=6
            ),
        ],
        className="mb-3"
    ),

    # ---- Row 2 ----
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Phone Number"),
                    dbc.Input(
                        id="p_phno",
                        type="tel",
                        pattern="[0-9]{10}",
                        className="mb-3"
                    )

                ],
                md=6
            ),
            dbc.Col(
                [
                    dbc.Label("Vehicle Number *"),
                    dbc.Input(id="p_vehicle"),
                ],
                md=6
            ),
        ],
        className="mb-3"
    ),

    # ---- Row 3 ----
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Item Name *"),
                    dbc.Select(
                        id="p_item",
                        options=[
                            {"label": "Iron Scrap", "value": "Iron Scrap"},
                            {"label": "Steel Scrap", "value": "Steel Scrap"},
                            {"label": "Aluminium", "value": "Aluminium"},
                            {"label": "Copper", "value": "Copper"},
                        ],
                    ),
                ],
                md=6
            ),
            dbc.Col(
                [
                    dbc.Label("Payment Status *"),
                    dbc.Select(
                        id="p_payment",
                        options=[
                            {"label": "Paid", "value": "Paid"},
                            {"label": "Pending", "value": "Pending"},
                        ],
                    ),
                ],
                md=6
            ),
        ],
        className="mb-3"
    ),

    # ---- Row 4 ----
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Tare Weight (KGs) *"),
                    dbc.Input(id="p_tare", type="number"),
                ],
                md=6
            ),
            dbc.Col(
                [
                    dbc.Label("Gross Weight (KGs) *"),
                    dbc.Input(id="p_gross", type="number"),
                ],
                md=6
            ),
        ],
        className="mb-3"
    ),

    # ---- Row 5 ----
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Net Weight (KGs)"),
                    dbc.Input(id="p_net", disabled=True),
                ],
                md=6
            ),
            dbc.Col(
                [
                    dbc.Label("Price (Per ton) *"),
                    dbc.Input(id="p_price", type="number"),
                ],
                md=6
            ),
        ],
        className="mb-3"
    ),

    # ---- Row 6 ----
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Total Amount"),
                    dbc.Input(id="p_total", disabled=True),
                ],
                md=6
            ),
            dbc.Col(),
        ],
        className="mb-3"
    ),

    dbc.Row(
        [
            dbc.Col(
                dbc.Button("Save Purchase", id="save_purchase", color="primary", className="w-100"),
                md=6
            ),
            dbc.Col(
                dbc.Button("Clear", id="clear_purchase", color="secondary", className="w-100"),
                md=6
            ),
        ],
        className="mb-3"
    ),

    html.Br(),
    dbc.Alert(id="purchase_output", is_open=False, duration=5000),
]

layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(form_content),
                className="shadow"
            ),
            md=6,
            sm=12
        ),
        justify="center",
        className="mt-4"
    ),
    fluid=True
)


@callback(
    Output("p_net", "value"),
    Output("p_total", "value"),
    Input("p_tare", "value"),
    Input("p_gross", "value"),
    Input("p_price", "value"),
    Input("clear_purchase", "n_clicks"),
    prevent_initial_call=True
)
def calculate_purchase_net_total(tare, gross, price, clear_click):
    ctx = callback_context

    if not ctx.triggered:
        return None, None

    trigger = ctx.triggered[0]["prop_id"]

    # Clear button clicked → reset net and total
    if "clear_purchase" in trigger:
        return None, None

    # Normal calculation
    if tare is None or gross is None:
        return None, None

    net_weight = gross - tare
    total_amount = round((net_weight / 1000) * price, 2) if price else None

    return net_weight, total_amount




@callback(
    Output("purchase_output", "children"),
    Output("purchase_output", "is_open"),
    Output("purchase_output", "color"),
    Input("save_purchase", "n_clicks"),
    State("p_date", "value"),
    State("p_vendor", "value"),
    State("p_phno", "value"),
    State("p_vehicle", "value"),
    State("p_item", "value"),
    State("p_tare", "value"),
    State("p_gross", "value"),
    State("p_net", "value"),
    State("p_price", "value"),
    State("p_total", "value"),
    State("p_payment", "value"),
)
def save_purchase(
    n, date_, vendor, phno, vehicle, item,
    tare, gross, net, price, total, payment
):
    if not n:
        return "", False, ""

    required = [vehicle, item, tare, gross, price, payment]
    if not all(required):
        return "❌ Please fill all required fields (*)", True, "warning"

    # Validate phone number
    if not validate_mobile_number(phno):
        return "❌ Enter a valid 10-digit phone number", True, "danger"

    # Validate vehicle number
    if not validate_vehicle_number(vehicle):
        return "❌ Invalid Vehicle Number", True, "danger"

    return f"✅ Purchase Saved | Total Amount = ₹{total}", True, "success"

@callback(
    Output("p_date", "value"),
    Output("p_vendor", "value"),
    Output("p_phno", "value"),
    Output("p_vehicle", "value"),
    Output("p_item", "value"),
    Output("p_tare", "value"),
    Output("p_gross", "value"),
    Output("p_price", "value"),
    Output("p_payment", "value"),
    Input("clear_purchase", "n_clicks"),
    prevent_initial_call=True
)
def clear_purchase_form(n):
    return (
        str(date.today()),
        None, None, None, None,
        None, None, None, None
    )

