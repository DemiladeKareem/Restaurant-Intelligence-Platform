
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"
rng = np.random.default_rng(303)

ingredients = pd.read_csv(OUT / "ingredients.csv")
products = pd.read_csv(OUT / "menu_products.csv")
orders = pd.read_csv(
    OUT / "orders.csv",
    usecols=["OrderID", "BranchID", "OrderDate"],
)
items = pd.read_csv(
    OUT / "order_items.csv",
    usecols=["OrderID", "ProductID", "Quantity"],
)
consumption = pd.read_csv(
    OUT / "production_consumption.csv"
)

START = pd.Timestamp("2025-10-01")
END = pd.Timestamp("2026-09-30")

# The model uses weekly replenishment.
# Requirements are based on generated operating demand.
# An 8% purchasing buffer helps avoid stock shortages.
BUFFER = 1.08

# Ingredient demand from kitchen production.
raw = consumption[
    ["ProductionDate", "FacilityID",
     "IngredientID", "QuantityConsumed"]
].copy()

raw = raw.rename(columns={
    "ProductionDate": "DemandDate",
    "QuantityConsumed": "RequiredQuantity",
})

# Purchased beverages and desserts are stocked directly.
purchased = products.loc[
    products["SupplyType"] == "Purchased",
    ["ProductID"],
].copy()

purchased["IngredientID"] = (
    "FG" + purchased["ProductID"].str[1:]
)

finished_demand = (
    items.merge(
        orders,
        on="OrderID",
        validate="many_to_one",
    )
    .merge(
        purchased,
        on="ProductID",
        how="inner",
        validate="many_to_one",
    )
)

finished_demand["FacilityID"] = (
    "FAC" + finished_demand["BranchID"].str[-3:]
)

finished_demand = finished_demand.rename(columns={
    "OrderDate": "DemandDate",
    "Quantity": "RequiredQuantity",
})

finished_demand = finished_demand[
    ["DemandDate", "FacilityID",
     "IngredientID", "RequiredQuantity"]
]

demand = pd.concat(
    [raw, finished_demand],
    ignore_index=True,
)

demand["DemandDate"] = pd.to_datetime(
    demand["DemandDate"]
)

# Seven-day replenishment periods starting October 1.
day_offset = (
    demand["DemandDate"] - START
).dt.days

demand["WeekNumber"] = day_offset // 7

weekly = (
    demand.groupby(
        ["WeekNumber", "FacilityID", "IngredientID"],
        as_index=False,
    )["RequiredQuantity"]
    .sum()
)

weekly["ReceiptDate"] = (
    START
    + pd.to_timedelta(
        weekly["WeekNumber"] * 7,
        unit="D",
    )
)

weekly["OrderQuantity"] = (
    weekly["RequiredQuantity"] * BUFFER
).round(3)

# Whole units for individually counted stock.
unit_lookup = ingredients.set_index(
    "IngredientID"
)["Unit"].to_dict()

whole_unit = weekly["IngredientID"].map(
    unit_lookup
).eq("piece")

weekly.loc[whole_unit, "OrderQuantity"] = np.ceil(
    weekly.loc[whole_unit, "OrderQuantity"]
)

# Small fractional quantities are rounded upward.
fractional_unit = ~whole_unit

weekly.loc[
    fractional_unit, "OrderQuantity"
] = (
    np.ceil(
        weekly.loc[
            fractional_unit, "OrderQuantity"
        ] * 1000
    ) / 1000
)

assert (weekly["OrderQuantity"] > 0).all()

# Supplier assignment is illustrative.
def assign_supplier(ingredient_id):
    if ingredient_id.startswith("FG"):
        return "SUP005"

    number = int(ingredient_id[3:])

    if number <= 16:
        return "SUP001"
    if number <= 26:
        return "SUP003"
    if number <= 32:
        return "SUP001"
    if number <= 44:
        return "SUP004"

    return "SUP006"


weekly["SupplierID"] = weekly[
    "IngredientID"
].map(assign_supplier)

weekly = weekly.merge(
    ingredients[
        ["IngredientID", "StandardCostNGN"]
    ],
    on="IngredientID",
    validate="many_to_one",
)

# Modest monthly cost changes and supplier variation.
month_index = (
    (weekly["ReceiptDate"].dt.year - 2025) * 12
    + weekly["ReceiptDate"].dt.month - 10
)

weekly["UnitCostNGN"] = (
    weekly["StandardCostNGN"]
    * (1 + month_index * 0.003)
    * rng.uniform(0.98, 1.02, len(weekly))
).round(2)

weekly["LineTotalNGN"] = (
    weekly["OrderQuantity"]
    * weekly["UnitCostNGN"]
).round(2)

# One purchase order per supplier, facility and week.
order_groups = (
    weekly[
        ["WeekNumber", "FacilityID",
         "SupplierID", "ReceiptDate"]
    ]
    .drop_duplicates()
    .sort_values(
        ["WeekNumber", "FacilityID", "SupplierID"]
    )
    .reset_index(drop=True)
)

order_groups["PurchaseOrderID"] = [
    f"PO{i:07d}"
    for i in range(1, len(order_groups) + 1)
]

# Purchase orders are placed three days before receipt.
# The first orders can precede the reporting period.
order_groups["PurchaseOrderDate"] = (
    order_groups["ReceiptDate"]
    - pd.Timedelta(days=3)
)

order_groups["GoodsReceiptID"] = [
    f"GR{i:07d}"
    for i in range(1, len(order_groups) + 1)
]

weekly = weekly.merge(
    order_groups[
        ["WeekNumber", "FacilityID", "SupplierID",
         "PurchaseOrderID", "GoodsReceiptID"]
    ],
    on=["WeekNumber", "FacilityID", "SupplierID"],
    validate="many_to_one",
)

purchase_orders = order_groups[
    ["PurchaseOrderID", "SupplierID", "FacilityID",
     "PurchaseOrderDate", "ReceiptDate"]
].copy()

purchase_orders["Status"] = "Received"

purchase_orders["PurchaseOrderDate"] = (
    purchase_orders["PurchaseOrderDate"]
    .dt.strftime("%Y-%m-%d")
)

purchase_orders["ReceiptDate"] = (
    purchase_orders["ReceiptDate"]
    .dt.strftime("%Y-%m-%d")
)

purchase_lines = weekly[
    ["PurchaseOrderID", "IngredientID",
     "OrderQuantity", "UnitCostNGN",
     "LineTotalNGN"]
].copy()

purchase_lines.insert(
    0,
    "PurchaseOrderLineID",
    [
        f"POL{i:08d}"
        for i in range(1, len(purchase_lines) + 1)
    ],
)

receipts = order_groups[
    ["GoodsReceiptID", "PurchaseOrderID",
     "FacilityID", "ReceiptDate"]
].copy()

receipts["ReceiptDate"] = (
    receipts["ReceiptDate"].dt.strftime("%Y-%m-%d")
)

receipt_lines = weekly[
    ["GoodsReceiptID", "IngredientID",
     "OrderQuantity", "UnitCostNGN"]
].copy()

receipt_lines = receipt_lines.rename(columns={
    "OrderQuantity": "ReceivedQuantity",
})

receipt_lines.insert(
    0,
    "GoodsReceiptLineID",
    [
        f"GRL{i:08d}"
        for i in range(1, len(receipt_lines) + 1)
    ],
)

# Check purchased stock covers generated demand.
coverage = weekly[
    ["FacilityID", "IngredientID", "WeekNumber",
     "OrderQuantity", "RequiredQuantity"]
]

assert (
    coverage["OrderQuantity"] + 0.000001
    >= coverage["RequiredQuantity"]
).all()

assert purchase_orders["PurchaseOrderID"].is_unique
assert receipts["GoodsReceiptID"].is_unique
assert purchase_lines["PurchaseOrderLineID"].is_unique
assert receipt_lines["GoodsReceiptLineID"].is_unique

purchase_orders.to_csv(
    OUT / "purchase_orders.csv", index=False
)
purchase_lines.to_csv(
    OUT / "purchase_order_lines.csv", index=False
)
receipts.to_csv(
    OUT / "goods_receipts.csv", index=False
)
receipt_lines.to_csv(
    OUT / "goods_receipt_lines.csv", index=False
)

print("Procurement generation complete.")
print(f"Purchase orders: {len(purchase_orders):,}")
print(f"Purchase order lines: {len(purchase_lines):,}")
print(f"Goods receipts: {len(receipts):,}")
print(f"Goods receipt lines: {len(receipt_lines):,}")
print("Procurement validations passed.")
