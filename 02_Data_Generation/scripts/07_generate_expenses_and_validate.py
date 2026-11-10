
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"
rng = np.random.default_rng(707)

branches = pd.read_csv(OUT / "branches.csv")
products = pd.read_csv(OUT / "menu_products.csv")
costs = pd.read_csv(OUT / "product_costs.csv")
orders = pd.read_csv(OUT / "orders.csv")
items = pd.read_csv(OUT / "order_items.csv")
payments = pd.read_csv(OUT / "payments.csv")
batches = pd.read_csv(OUT / "production_batches.csv")
consumption = pd.read_csv(
    OUT / "production_consumption.csv"
)
ingredients = pd.read_csv(OUT / "ingredients.csv")
movements = pd.read_csv(
    OUT / "inventory_movements.csv"
)
reconciliation = pd.read_csv(
    OUT / "inventory_reconciliation.csv"
)
exceptions = pd.read_csv(
    OUT / "inventory_stock_exceptions.csv"
)

months = pd.period_range(
    "2025-10", "2026-09", freq="M"
)

# Monthly operating expenses in synthetic NGN.
expense_baselines = {
    "Rent": 650000,
    "Labour": 2800000,
    "Electricity": 420000,
    "Generator Fuel": 580000,
    "Cleaning": 150000,
    "Maintenance": 180000,
    "Internet": 75000,
    "Security": 180000,
}

branch_factors = {
    "BR001": 1.00,
    "BR002": 1.18,
    "BR003": 0.83,
    "BR004": 0.94,
    "BR005": 1.10,
}

expense_rows = []

for branch_id in branches["BranchID"]:
    factor = branch_factors[branch_id]

    for month_index, month in enumerate(months):
        for category, baseline in expense_baselines.items():
            inflation = 1 + month_index * 0.004
            variation = rng.uniform(0.95, 1.05)

            amount = round(
                baseline * factor * inflation * variation,
                2,
            )

            expense_rows.append({
                "ExpenseID": (
                    f"EXP{len(expense_rows) + 1:07d}"
                ),
                "BranchID": branch_id,
                "ExpenseMonth": str(month),
                "ExpenseCategory": category,
                "AmountNGN": amount,
            })

expenses = pd.DataFrame(expense_rows)

expenses.to_csv(
    OUT / "operating_expenses.csv",
    index=False,
)

# --------------------------------------------------
# Data quality validation
# --------------------------------------------------

checks = {}

checks["Unique order IDs"] = (
    orders["OrderID"].is_unique
)

checks["Unique sales line IDs"] = (
    items["OrderItemID"].is_unique
)

checks["Every order has one payment"] = (
    payments["OrderID"].is_unique
    and set(orders["OrderID"]) == set(payments["OrderID"])
)

checks["Order revenue equals payments"] = np.isclose(
    orders["NetAmountNGN"].sum(),
    payments["PaymentAmountNGN"].sum(),
    atol=0.01,
)

checks["Order revenue equals sales lines"] = np.isclose(
    orders["NetAmountNGN"].sum(),
    items["NetAmountNGN"].sum(),
    atol=0.01,
)

checks["No missing product costs"] = (
    set(items["ProductID"]).issubset(
        set(costs["ProductID"])
    )
)

checks["All product costs positive"] = (
    costs["StandardUnitCostNGN"].gt(0).all()
)

checks["Production quantities valid"] = (
    batches["ProducedPortions"].gt(0).all()
    and batches["WastePortions"].ge(0).all()
    and (
        batches["ProducedPortions"]
        == (
            batches["SoldPortions"]
            + batches["WastePortions"]
        )
    ).all()
)

checks["Ingredient consumption positive"] = (
    consumption["QuantityConsumed"].gt(0).all()
)

checks["No negative stock"] = (
    exceptions.empty
    and movements["RunningBalance"].ge(-0.00001).all()
)

checks["Inventory reconciliation balances"] = (
    np.allclose(
        reconciliation["NetMovement"],
        reconciliation["ClosingBalance"],
        atol=0.00001,
    )
)

checks["Expenses valid"] = (
    expenses["ExpenseID"].is_unique
    and expenses["AmountNGN"].gt(0).all()
)

checks["Expected reporting period"] = (
    orders["OrderDate"].min() == "2025-10-01"
    and orders["OrderDate"].max() == "2026-09-30"
)

# --------------------------------------------------
# Estimated branch profitability
# --------------------------------------------------

sales_costs = items.merge(
    costs,
    on="ProductID",
    how="left",
    validate="many_to_one",
)

sales_costs["StandardCOGSNGN"] = (
    sales_costs["Quantity"]
    * sales_costs["StandardUnitCostNGN"]
)

sales_costs = sales_costs.merge(
    orders[["OrderID", "BranchID", "OrderDate"]],
    on="OrderID",
    validate="many_to_one",
)

sales_costs["Month"] = (
    sales_costs["OrderDate"].str[:7]
)

monthly_sales = (
    sales_costs.groupby(
        ["BranchID", "Month"],
        as_index=False,
    )
    .agg(
        RevenueNGN=("NetAmountNGN", "sum"),
        StandardCOGSNGN=("StandardCOGSNGN", "sum"),
    )
)

monthly_expenses = (
    expenses.groupby(
        ["BranchID", "ExpenseMonth"],
        as_index=False,
    )["AmountNGN"]
    .sum()
    .rename(columns={
        "ExpenseMonth": "Month",
        "AmountNGN": "OperatingExpensesNGN",
    })
)

profitability = monthly_sales.merge(
    monthly_expenses,
    on=["BranchID", "Month"],
    how="left",
    validate="one_to_one",
)

profitability["GrossProfitNGN"] = (
    profitability["RevenueNGN"]
    - profitability["StandardCOGSNGN"]
)

profitability["EstimatedOperatingProfitNGN"] = (
    profitability["GrossProfitNGN"]
    - profitability["OperatingExpensesNGN"]
)

profitability["EstimatedOperatingMarginPct"] = (
    100
    * profitability["EstimatedOperatingProfitNGN"]
    / profitability["RevenueNGN"].replace(0, np.nan)
).round(2)

checks["All monthly expenses matched"] = (
    profitability["OperatingExpensesNGN"].notna().all()
)

checks["Profit calculation reconciles"] = (
    np.allclose(
        profitability["EstimatedOperatingProfitNGN"],
        profitability["RevenueNGN"]
        - profitability["StandardCOGSNGN"]
        - profitability["OperatingExpensesNGN"],
        atol=0.01,
    )
)

profitability.to_csv(
    OUT / "monthly_branch_profitability.csv",
    index=False,
)

# --------------------------------------------------
# Validation report
# --------------------------------------------------

report = pd.DataFrame([
    {
        "ValidationCheck": name,
        "Status": "PASS" if passed else "FAIL",
    }
    for name, passed in checks.items()
])

report.to_csv(
    OUT / "validation_report.csv",
    index=False,
)

print("\nFINAL DATA VALIDATION")
print("-" * 55)

for name, passed in checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {name}")

print("-" * 55)
print(f"Operating expense records: {len(expenses):,}")
print(f"Monthly profitability records: {len(profitability):,}")
print(f"Total customer orders: {len(orders):,}")
print(f"Total revenue: NGN {orders['NetAmountNGN'].sum():,.2f}")
print(
    "Estimated operating profit: NGN "
    f"{profitability['EstimatedOperatingProfitNGN'].sum():,.2f}"
)

failed = [
    name for name, passed in checks.items()
    if not passed
]

if failed:
    raise ValueError(
        f"{len(failed)} validation checks failed: "
        + ", ".join(failed)
    )

print("\nALL FINAL VALIDATIONS PASSED.")
