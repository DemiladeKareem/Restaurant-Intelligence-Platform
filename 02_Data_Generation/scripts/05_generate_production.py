
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"

products = pd.read_csv(OUT / "menu_products.csv")
orders = pd.read_csv(
    OUT / "orders.csv",
    usecols=["OrderID", "BranchID", "OrderDate"],
)
items = pd.read_csv(
    OUT / "order_items.csv",
    usecols=["OrderID", "ProductID", "Quantity"],
)
recipes = pd.read_csv(OUT / "recipes.csv")
components = pd.read_csv(OUT / "recipe_components.csv")

# Connect sold products to their branch and sale date.
sales = items.merge(
    orders,
    on="OrderID",
    validate="many_to_one",
)

sales = sales.merge(
    products[["ProductID", "SupplyType"]],
    on="ProductID",
    validate="many_to_one",
)

daily_demand = (
    sales.groupby(
        ["OrderDate", "BranchID", "ProductID", "SupplyType"],
        as_index=False,
    )["Quantity"]
    .sum()
    .rename(columns={"Quantity": "SoldPortions"})
)

prepared = daily_demand.loc[
    daily_demand["SupplyType"].isin(
        ["Branch", "Central"]
    )
].copy()

branch_prepared = prepared.loc[
    prepared["SupplyType"] == "Branch"
].copy()

central_prepared = prepared.loc[
    prepared["SupplyType"] == "Central"
].copy()

# Branch kitchens produce a modest amount above demand.
branch_prepared["ProducedPortions"] = np.ceil(
    branch_prepared["SoldPortions"] * 1.03
).astype(int)

branch_prepared["WastePortions"] = (
    branch_prepared["ProducedPortions"]
    - branch_prepared["SoldPortions"]
)

branch_prepared["FacilityID"] = (
    "FAC" + branch_prepared["BranchID"].str[-3:]
)

branch_prepared["TransferredPortions"] = 0

# The central kitchen supplies finished products to branches.
# Each transfer matches the receiving branch's daily demand.
transfers = central_prepared[
    ["OrderDate", "BranchID", "ProductID", "SoldPortions"]
].copy()

transfers = transfers.rename(columns={
    "OrderDate": "TransferDate",
    "SoldPortions": "TransferQuantity",
})

transfers["FromFacilityID"] = "FAC006"
transfers["ToFacilityID"] = (
    "FAC" + transfers["BranchID"].str[-3:]
)

transfers.insert(
    0,
    "TransferID",
    [
        f"TR{i:08d}"
        for i in range(1, len(transfers) + 1)
    ],
)

# Consolidate central kitchen production by product and day.
central_batches = (
    central_prepared.groupby(
        ["OrderDate", "ProductID"],
        as_index=False,
    )["SoldPortions"]
    .sum()
)

central_batches["ProducedPortions"] = np.ceil(
    central_batches["SoldPortions"] * 1.02
).astype(int)

central_batches["WastePortions"] = (
    central_batches["ProducedPortions"]
    - central_batches["SoldPortions"]
)

central_batches["TransferredPortions"] = (
    central_batches["SoldPortions"]
)

central_batches["FacilityID"] = "FAC006"
central_batches["BranchID"] = ""

batch_columns = [
    "OrderDate",
    "FacilityID",
    "BranchID",
    "ProductID",
    "ProducedPortions",
    "SoldPortions",
    "TransferredPortions",
    "WastePortions",
]

batches = pd.concat(
    [
        branch_prepared[batch_columns],
        central_batches[batch_columns],
    ],
    ignore_index=True,
)

batches = batches.rename(columns={
    "OrderDate": "ProductionDate",
})

batches.insert(
    0,
    "BatchID",
    [
        f"BAT{i:08d}"
        for i in range(1, len(batches) + 1)
    ],
)

batches = batches.merge(
    recipes[["RecipeID", "ProductID"]],
    on="ProductID",
    how="left",
    validate="many_to_one",
)

assert batches["RecipeID"].notna().all(), (
    "Some prepared products have no recipe."
)

# Each batch consumes ingredients for all portions produced,
# including portions later classified as waste.
consumption = batches[
    [
        "BatchID",
        "ProductionDate",
        "FacilityID",
        "RecipeID",
        "ProducedPortions",
    ]
].merge(
    components[
        ["RecipeID", "IngredientID", "QuantityPerPortion"]
    ],
    on="RecipeID",
    validate="many_to_many",
)

consumption["QuantityConsumed"] = (
    consumption["ProducedPortions"]
    * consumption["QuantityPerPortion"]
).round(5)

consumption.insert(
    0,
    "ConsumptionID",
    [
        f"PC{i:09d}"
        for i in range(1, len(consumption) + 1)
    ],
)

consumption = consumption[
    [
        "ConsumptionID",
        "BatchID",
        "ProductionDate",
        "FacilityID",
        "IngredientID",
        "QuantityConsumed",
    ]
]

transfers = transfers[
    [
        "TransferID",
        "TransferDate",
        "FromFacilityID",
        "ToFacilityID",
        "BranchID",
        "ProductID",
        "TransferQuantity",
    ]
]

# Validate production against sales.
assert (batches["ProducedPortions"] > 0).all()
assert (batches["WastePortions"] >= 0).all()
assert (consumption["QuantityConsumed"] > 0).all()
assert batches["BatchID"].is_unique
assert transfers["TransferID"].is_unique

assert (
    batches["ProducedPortions"]
    == (
        batches["SoldPortions"]
        + batches["WastePortions"]
    )
).all()

assert (
    central_batches["TransferredPortions"].sum()
    == transfers["TransferQuantity"].sum()
)

assert (
    batches.loc[
        batches["FacilityID"] == "FAC006",
        "SoldPortions",
    ].sum()
    == transfers["TransferQuantity"].sum()
)

batches.to_csv(
    OUT / "production_batches.csv", index=False
)

consumption.to_csv(
    OUT / "production_consumption.csv", index=False
)

transfers.to_csv(
    OUT / "stock_transfers.csv", index=False
)

print("Production generation complete.")
print(f"Production batches: {len(batches):,}")
print(f"Ingredient consumption records: {len(consumption):,}")
print(f"Central kitchen transfers: {len(transfers):,}")
print("Production validations passed.")
