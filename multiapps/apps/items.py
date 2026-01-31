from dash import html, dash_table
import dash_bootstrap_components as dbc

from dash import html, dash_table
import dash_bootstrap_components as dbc

item_master_layout = dbc.Container(
    [
        html.H3("Item Master", className="text-center mb-4"),

        dbc.Row(
            [
                # ---------- LEFT : ACCORDION ----------
                dbc.Col(
                    dbc.Accordion(
                        [
                            # ---- ADD ITEM ----
                            dbc.AccordionItem(
                                [
                                    dbc.Label("Item Name *"),
                                    dbc.Input(id="item_name", className="mb-3"),

                                    dbc.Label("Price (Per ton) *"),
                                    dbc.Input(id="item_price", type="number", className="mb-3"),

                                    dbc.Button(
                                        "Add Item",
                                        id="add_item",
                                        color="primary",
                                        className="w-100"
                                    ),

                                    html.Br(),
                                    dbc.Alert(id="item_msg", is_open=False),
                                ],
                                title="➕ Add New Item"
                            ),

                            # ---- UPDATE PRICE ----
                            dbc.AccordionItem(
                                [
                                    dbc.Label("Select Item *"),
                                    dbc.Select(
                                        id="update_item_name",
                                        options=[],
                                        className="mb-3"
                                    ),

                                    dbc.Label("New Price (Per ton) *"),
                                    dbc.Input(
                                        id="update_item_price",
                                        type="number",
                                        className="mb-3"
                                    ),

                                    dbc.Button(
                                        "Update Price",
                                        id="update_item_btn",
                                        color="warning",
                                        className="w-100"
                                    ),

                                    html.Br(),
                                    dbc.Alert(id="update_item_msg", is_open=False),
                                ],
                                title="✏️ Update Item Price"
                            ),
                        ],
                        start_collapsed=True,
                        flush=True,
                    ),
                    md=4
                ),

                # ---------- RIGHT : ITEMS TABLE ----------
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Items List", className="mb-3"),

                                dash_table.DataTable(
                                    id="item_table",
                                    columns=[
                                        {"name": "Item Name", "id": "name"},
                                        {"name": "Price / Ton", "id": "price"},
                                        {"name": "Last Updated", "id": "last_updated"},
                                        {"name": "Updated By", "id": "updated_by"},
                                    ],
                                    data=[],
                                    page_size=8,
                                    style_table={"overflowX": "auto"},
                                    style_header={
                                        "backgroundColor": "#f1f3f5",
                                        "fontWeight": "bold",
                                        "textAlign": "left",
                                    },
                                    style_cell={
                                        "padding": "10px",
                                        "border": "1px solid #dee2e6",
                                        "fontSize": "14px",
                                    },
                                    style_data_conditional=[
                                        {
                                            "if": {"row_index": "odd"},
                                            "backgroundColor": "#fafafa",
                                        }
                                    ],
                                )

                            ]
                        ),
                        className="shadow-sm"
                    ),
                    md=8
                ),
            ],
            className="g-4"
        ),
    ],
    fluid=True
)



layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(item_master_layout),
                className="shadow"
            ),
            md=10,
            sm=12
        ),
        justify="center",
        className="mt-4"
    ),
    fluid=True
)