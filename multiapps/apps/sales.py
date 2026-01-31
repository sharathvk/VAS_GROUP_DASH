from dash import html, Input, Output, State, callback, callback_context
import dash_bootstrap_components as dbc
from datetime import date
from multiapps.utils.validations import validate_mobile_number, validate_vehicle_number


# ------------------ Layout ------------------
form_content = [
    html.H3("Sales Entry", className="text-center mb-4"),

    # ---- Row 1 ----
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Date"),
                    dbc.Input(type="date", id="s_date", value=str(date.today())),
                ],
                md=6
            ),
            dbc.Col(
                [
                    dbc.Label("Customer Name"),
                    dbc.Input(id="s_customer"),
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
                        id="s_phno",
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
                    dbc.Input(id="s_vehicle"),
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
                        id="s_item",
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
                        id="s_payment",
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
                    dbc.Input(id="s_tare", type="number"),
                ],
                md=6
            ),
            dbc.Col(
                [
                    dbc.Label("Gross Weight (KGs) *"),
                    dbc.Input(id="s_gross", type="number"),
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
                    dbc.Input(id="s_net", disabled=True),
                ],
                md=6
            ),
            dbc.Col(
                [
                    dbc.Label("Price (Per ton) *"),
                    dbc.Input(id="s_price", type="number"),
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
                    dbc.Input(id="s_total", disabled=True),
                ],
                md=6
            ),
            dbc.Col(),  # empty column for alignment
        ],
        className="mb-3"
    ),

    dbc.Row(
        [
            dbc.Col(
                dbc.Button("Save Sale", id="save_sale", color="success", className="w-100"),
                md=6
            ),
            dbc.Col(
                dbc.Button("Clear", id="clear_sale", color="secondary", className="w-100"),
                md=6
            ),
        ],
        className="mb-3"
    ),

    html.Br(),
    dbc.Alert(id="sale_output", is_open=False, duration=5000),
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

# ------------------ Auto Calculation ------------------
@callback(
    Output("s_net", "value"),
    Output("s_total", "value"),
    Input("s_tare", "value"),
    Input("s_gross", "value"),
    Input("s_price", "value"),
    Input("clear_sale", "n_clicks"),
    prevent_initial_call=True
)
def calculate_or_clear(tare, gross, price, clear_click):
    ctx = callback_context

    if not ctx.triggered:
        return None, None

    trigger = ctx.triggered[0]["prop_id"]

    # Clear button clicked → reset values
    if "clear_sale" in trigger:
        return None, None

    # Normal calculation
    if tare is None or gross is None:
        return None, None

    net_weight = gross - tare
    total_amount = round((net_weight / 1000) * price, 2) if price else None

    return net_weight, total_amount


# ------------------ Save Sale ------------------
@callback(
    Output("sale_output", "children"),
    Output("sale_output", "is_open"),
    Output("sale_output", "color"),
    Input("save_sale", "n_clicks"),
    State("s_date", "value"),
    State("s_customer", "value"),
    State("s_phno", "value"),
    State("s_vehicle", "value"),
    State("s_item", "value"),
    State("s_tare", "value"),
    State("s_gross", "value"),
    State("s_net", "value"),
    State("s_price", "value"),
    State("s_total", "value"),
    State("s_payment", "value"),
)
def save_sale(
    n, date_, customer, phno, vehicle, item,
    tare, gross, net, price, total, payment
):
    if not n:
        return "", False, ''

    required = [vehicle, item, tare, gross, price, payment]
    if not all(required):
        return "❌ Please fill all required fields (*)", True, "warning"

    # Validate phone number
    if not validate_mobile_number(phno):
        return "❌ Enter a valid 10-digit phone number", True, "danger"

    # Validate vehicle number
    if not validate_vehicle_number(vehicle):
        return "❌ Invalid Vehicle Number", True, "danger"

    return f"✅ Sale Saved Successfully | Total Amount = ₹{total}", True, "success"

# ---------------- Clear sale fields ------------
@callback(
    Output("s_date", "value"),
    Output("s_customer", "value"),
    Output("s_phno", "value"),
    Output("s_vehicle", "value"),
    Output("s_item", "value"),
    Output("s_tare", "value"),
    Output("s_gross", "value"),
    Output("s_price", "value"),
    Output("s_payment", "value"),
    Input("clear_sale", "n_clicks"),
    prevent_initial_call=True
)
def clear_sale_form(n):
    return (
        str(date.today()),  # reset date to today
        None,  # vendor
        None,  # phone
        None,  # vehicle
        None,  # item
        None,  # tare
        None,  # gross
        None,  # price
        None   # payment
    )



