
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"

ingredients = pd.read_csv(OUT / "ingredients.csv")
products = pd.read_csv(OUT / "menu_products.csv")
receipts = pd.read_csv(OUT / "goods_receipts.csv")
receipt_lines = pd.read_csv(
    OUT / "goods_receipt_lines.csv"
)
consumption = pd.read_csv(
    OUT / "production_consumption.csv"
)
batches = pd.read_csv(
    OUT / "production_batches.csv"
)
transfers = pd.read_csv(
    OUT / "stock_transfers.csv"
)
orders = pd.read_csv(
    OUT / "orders.csv",
    usecols=["OrderID", "BranchID", "OrderDate"],
)
items = pd.read_csv(
    OUT / "order_items.csv",
    usecols=["OrderID", "ProductID", "Quantity"],
)

movement_parts = []

def add_movements(
    frame, date_col, facility_col,
    item_col, quantity_col, movement_type, priority
):
    if frame.empty:
        return

    part = frame[
        [date_col, facility_col, item_col, quantity_col]
    ].copy()

    part.columns = [
        "MovementDate",
        "FacilityID",
        "StockItemID",
        "QuantityChange",
    ]

    part["MovementType"] = movement_type
    part["Priority"] = priority

    movement_parts.append(part)


# 1. Goods received at the beginning of each week.
received = receipt_lines.merge(
    receipts[
        ["GoodsReceiptID", "FacilityID", "ReceiptDate"]
    ],
    on="GoodsReceiptID",
    validate="many_to_one",
)

add_movements(
    received,
    "ReceiptDate",
    "FacilityID",
    "IngredientID",
    "ReceivedQuantity",
    "Goods Receipt",
    10,
)

# 2. Kitchen ingredients consumed during production.
consumed = consumption.copy()
consumed["QuantityChange"] = (
    -consumed["QuantityConsumed"]
)

add_movements(
    consumed,
    "ProductionDate",
    "FacilityID",
    "IngredientID",
    "QuantityChange",
    "Production Consumption",
    20,
)

# 3. Central kitchen creates finished products.
central = batches.loc[
    batches["FacilityID"] == "FAC006"
].copy()

central["StockItemID"] = (
    "FP" + central["ProductID"].str[1:]
)

add_movements(
    central.assign(
        QuantityChange=central["ProducedPortions"]
    ),
    "ProductionDate",
    "FacilityID",
    "StockItemID",
    "QuantityChange",
    "Finished Production",
    30,
)

# 4. Surplus central-kitchen portions are discarded.
add_movements(
    central.assign(
        QuantityChange=-central["WastePortions"]
    ),
    "ProductionDate",
    "FacilityID",
    "StockItemID",
    "QuantityChange",
    "Production Waste",
    35,
)

# 5. Finished products leave the central kitchen.
transfers["StockItemID"] = (
    "FP" + transfers["ProductID"].str[1:]
)

add_movements(
    transfers.assign(
        QuantityChange=-transfers["TransferQuantity"]
    ),
    "TransferDate",
    "FromFacilityID",
    "StockItemID",
    "QuantityChange",
    "Transfer Out",
    40,
)

# 6. Finished products arrive at branch kitchens.
add_movements(
    transfers.rename(columns={
        "ToFacilityID": "ReceivingFacilityID"
    }),
    "TransferDate",
    "ReceivingFacilityID",
    "StockItemID",
    "TransferQuantity",
    "Transfer In",
    50,
)

# 7. Sales of centrally produced and purchased items.
sales = (
    items.merge(
        orders,
        on="OrderID",
        validate="many_to_one",
    )
    .merge(
        products[["ProductID", "SupplyType"]],
        on="ProductID",
        validate="many_to_one",
    )
)

stocked_sales = sales.loc[
    sales["SupplyType"].isin(
        ["Central", "Purchased"]
    )
].copy()

stocked_sales["FacilityID"] = (
    "FAC" + stocked_sales["BranchID"].str[-3:]
)

stocked_sales["StockItemID"] = np.where(
    stocked_sales["SupplyType"] == "Central",
    "FP" + stocked_sales["ProductID"].str[1:],
    "FG" + stocked_sales["ProductID"].str[1:],
)

stocked_sales["QuantityChange"] = (
    -stocked_sales["Quantity"]
)

add_movements(
    stocked_sales,
    "OrderDate",
    "FacilityID",
    "StockItemID",
    "QuantityChange",
    "Customer Sale",
    60,
)

# Consolidate movement rows without losing movement types.
movements = pd.concat(
    movement_parts,
    ignore_index=True,
)

movements["MovementDate"] = pd.to_datetime(
    movements["MovementDate"]
)

movements["QuantityChange"] = (
    movements["QuantityChange"].astype(float)
)

movements = (
    movements.groupby(
        [
            "MovementDate",
            "FacilityID",
            "StockItemID",
            "MovementType",
            "Priority",
        ],
        as_index=False,
    )["QuantityChange"]
    .sum()
)

movements = movements.loc[
    movements["QuantityChange"].abs() > 0.0000001
].copy()

movements = movements.sort_values(
    [
        "MovementDate",
        "Priority",
        "FacilityID",
        "StockItemID",
    ]
).reset_index(drop=True)

# Inventory starts at zero. Weekly goods receipts are
# recorded before production and customer sales.
movements["RunningBalance"] = (
    movements.groupby(
        ["FacilityID", "StockItemID"]
    )["QuantityChange"]
    .cumsum()
    .round(5)
)

movements["MovementDate"] = (
    movements["MovementDate"].dt.strftime("%Y-%m-%d")
)

movements.insert(
    0,
    "MovementID",
    [
        f"IM{i:09d}"
        for i in range(1, len(movements) + 1)
    ],
)

exceptions = movements.loc[
    movements["RunningBalance"] < -0.00001
].copy()

# Verify each item's closing balance.
reconciliation = (
    movements.groupby(
        ["FacilityID", "StockItemID"],
        as_index=False,
    )
    .agg(
        NetMovement=("QuantityChange", "sum"),
        ClosingBalance=("RunningBalance", "last"),
    )
)

reconciliation["Difference"] = (
    reconciliation["NetMovement"]
    - reconciliation["ClosingBalance"]
).round(5)

assert np.allclose(
    reconciliation["Difference"],
    0,
    atol=0.00001,
)

assert movements["MovementID"].is_unique
assert (movements["FacilityID"].notna()).all()
assert (movements["StockItemID"].notna()).all()

# Export even if exceptions exist so they can be examined.
movements.to_csv(
    OUT / "inventory_movements.csv", index=False
)
reconciliation.to_csv(
    OUT / "inventory_reconciliation.csv", index=False
)
exceptions.to_csv(
    OUT / "inventory_stock_exceptions.csv", index=False
)

print("Inventory generation complete.")
print(f"Inventory movements: {len(movements):,}")
print(f"Reconciled stock items: {len(reconciliation):,}")
print(f"Negative stock exceptions: {len(exceptions):,}")

if len(exceptions) > 0:
    raise ValueError(
        f"Inventory contains {len(exceptions):,} "
        "negative stock exceptions. "
        "Check inventory_stock_exceptions.csv."
    )

print("Inventory validations passed.")
