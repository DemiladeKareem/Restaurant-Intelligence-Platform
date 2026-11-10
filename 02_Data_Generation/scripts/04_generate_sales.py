
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(20261021)

branches = pd.read_csv(OUT / "branches.csv")
products = pd.read_csv(OUT / "menu_products.csv")
variants = pd.read_csv(OUT / "product_variants.csv")

dates = pd.date_range("2025-10-01", "2026-09-30")

# Synthetic operating assumptions, not actual restaurant records.
branch_demand = {
    "BR001": 185,
    "BR002": 230,
    "BR003": 145,
    "BR004": 175,
    "BR005": 205,
}

channels = [
    "Dine-In",
    "Walk-In Takeaway",
    "Delivery",
    "Preorder",
]
channel_weights = [0.40, 0.35, 0.20, 0.05]

payment_methods = [
    "POS",
    "Bank Transfer",
    "Cash",
    "Online",
]
payment_weights = [0.45, 0.30, 0.15, 0.10]

# Keep the model simple: one standard variant per product.
catalogue = products.merge(
    variants[["VariantID", "ProductID"]],
    on="ProductID",
    validate="one_to_one",
)

product_ids = catalogue["ProductID"].to_numpy()
variant_ids = catalogue["VariantID"].to_numpy()
base_prices = catalogue["BasePriceNGN"].to_numpy(
    dtype=float
)

# Food is purchased more often than drinks and desserts.
category_weights = {
    "Rice": 1.8,
    "Pasta": 1.2,
    "Swallow": 1.1,
    "Soup": 1.2,
    "Protein": 1.5,
    "Sides": 1.0,
    "Bakery": 1.4,
    "Beverage": 2.0,
    "Dessert": 0.6,
    "Specials": 0.9,
}

weights = catalogue["Category"].map(
    category_weights
).to_numpy(dtype=float)

# Assignment, not in-place division: compatible with
# read-only NumPy arrays.
weights = weights / weights.sum()

orders_parts = []
items_parts = []
payments_parts = []
price_rows = []

order_counter = 0
item_counter = 0

branch_factors = {
    "BR001": 1.00,
    "BR002": 1.04,
    "BR003": 0.97,
    "BR004": 1.00,
    "BR005": 1.03,
}

# Monthly menu price history.
months = pd.period_range(
    "2025-10", "2026-09", freq="M"
)

for month_index, month in enumerate(months):
    inflation_factor = 1 + (0.004 * month_index)

    for branch_id in branch_demand:
        factor = branch_factors[branch_id]

        for i, product_id in enumerate(product_ids):
            price = round(
                base_prices[i] * factor * inflation_factor
                / 50
            ) * 50

            price_rows.append({
                "PriceID": (
                    f"PR{len(price_rows) + 1:07d}"
                ),
                "BranchID": branch_id,
                "ProductID": product_id,
                "VariantID": variant_ids[i],
                "PriceMonth": str(month),
                "UnitPriceNGN": float(price),
            })

prices_df = pd.DataFrame(price_rows)
prices_df.to_csv(
    OUT / "menu_prices.csv", index=False
)

price_lookup = {
    (row.BranchID, row.PriceMonth): group.sort_values(
        "ProductID"
    )["UnitPriceNGN"].to_numpy(dtype=float)
    for (branch_id, month), group in prices_df.groupby(
        ["BranchID", "PriceMonth"], sort=False
    )
    for row in [
        type("Key", (), {
            "BranchID": branch_id,
            "PriceMonth": month,
        })()
    ]
}

# Ensure product indices align with catalogue order.
price_lookup = {}
for (branch_id, month), group in prices_df.groupby(
    ["BranchID", "PriceMonth"]
):
    aligned = catalogue[["ProductID"]].merge(
        group[["ProductID", "UnitPriceNGN"]],
        on="ProductID",
        validate="one_to_one",
    )
    price_lookup[(branch_id, month)] = aligned[
        "UnitPriceNGN"
    ].to_numpy(dtype=float)

for date in dates:
    date_string = date.strftime("%Y-%m-%d")
    month_string = date.strftime("%Y-%m")

    weekend_factor = 1.25 if date.dayofweek >= 5 else 1.0

    # Moderate year-end and holiday demand variation.
    seasonal_factor = (
        1.18 if date.month == 12
        else 1.08 if date.month in (4, 8)
        else 1.0
    )

    for branch_id, baseline in branch_demand.items():
        expected_orders = (
            baseline * weekend_factor * seasonal_factor
        )

        order_count = int(rng.poisson(expected_orders))
        if order_count == 0:
            continue

        order_numbers = np.arange(
            order_counter + 1,
            order_counter + order_count + 1,
        )
        order_counter += order_count

        order_ids = np.char.add(
            "ORD",
            np.char.zfill(order_numbers.astype(str), 8),
        )

        channel_values = rng.choice(
            channels,
            size=order_count,
            p=channel_weights,
        )

        payment_values = rng.choice(
            payment_methods,
            size=order_count,
            p=payment_weights,
        )

        # A transaction can contain one, two or three items.
        line_counts = rng.choice(
            [1, 2, 3],
            size=order_count,
            p=[0.43, 0.42, 0.15],
        )

        total_lines = int(line_counts.sum())
        parent_index = np.repeat(
            np.arange(order_count),
            line_counts,
        )

        chosen = rng.choice(
            len(product_ids),
            size=total_lines,
            p=weights,
        )

        quantities = rng.choice(
            [1, 2, 3],
            size=total_lines,
            p=[0.86, 0.12, 0.02],
        )

        unit_prices = price_lookup[
            (branch_id, month_string)
        ][chosen]

        line_gross = quantities * unit_prices

        # Small promotional discount on selected orders.
        discount_rates = rng.choice(
            [0.0, 0.05, 0.10],
            size=order_count,
            p=[0.88, 0.09, 0.03],
        )

        line_discounts = np.round(
            line_gross * discount_rates[parent_index], 2
        )
        line_net = line_gross - line_discounts

        gross_by_order = np.bincount(
            parent_index,
            weights=line_gross,
            minlength=order_count,
        )

        discount_by_order = np.bincount(
            parent_index,
            weights=line_discounts,
            minlength=order_count,
        )

        net_by_order = gross_by_order - discount_by_order

        hours = rng.choice(
            [8, 9, 10, 11, 12, 13, 14, 15,
             16, 17, 18, 19, 20, 21],
            size=order_count,
            p=np.array([
                3, 4, 4, 7, 13, 14, 9, 6,
                5, 7, 10, 9, 6, 3,
            ]) / 100,
        )

        minutes = rng.integers(
            0, 60, size=order_count
        )

        timestamps = [
            f"{date_string} {h:02d}:{m:02d}:00"
            for h, m in zip(hours, minutes)
        ]

        orders_parts.append(pd.DataFrame({
            "OrderID": order_ids,
            "BranchID": branch_id,
            "OrderDate": date_string,
            "OrderTimestamp": timestamps,
            "SalesChannel": channel_values,
            "GrossAmountNGN": gross_by_order,
            "DiscountAmountNGN": discount_by_order,
            "NetAmountNGN": net_by_order,
        }))

        line_numbers = np.arange(
            item_counter + 1,
            item_counter + total_lines + 1,
        )
        item_counter += total_lines

        item_ids = np.char.add(
            "OI",
            np.char.zfill(line_numbers.astype(str), 9),
        )

        items_parts.append(pd.DataFrame({
            "OrderItemID": item_ids,
            "OrderID": order_ids[parent_index],
            "ProductID": product_ids[chosen],
            "VariantID": variant_ids[chosen],
            "Quantity": quantities,
            "UnitPriceNGN": unit_prices,
            "GrossAmountNGN": line_gross,
            "DiscountAmountNGN": line_discounts,
            "NetAmountNGN": line_net,
        }))

        payments_parts.append(pd.DataFrame({
            "PaymentID": np.char.add(
                "PAY",
                np.char.zfill(
                    order_numbers.astype(str), 8
                ),
            ),
            "OrderID": order_ids,
            "PaymentMethod": payment_values,
            "PaymentAmountNGN": net_by_order,
            "PaymentStatus": "Completed",
        }))

orders = pd.concat(orders_parts, ignore_index=True)
items = pd.concat(items_parts, ignore_index=True)
payments = pd.concat(payments_parts, ignore_index=True)

assert orders["OrderID"].is_unique
assert items["OrderItemID"].is_unique
assert payments["OrderID"].is_unique
assert (orders["NetAmountNGN"] >= 0).all()

assert np.allclose(
    orders["NetAmountNGN"].sum(),
    payments["PaymentAmountNGN"].sum(),
)

assert np.allclose(
    orders["NetAmountNGN"].sum(),
    items["NetAmountNGN"].sum(),
)

orders.to_csv(OUT / "orders.csv", index=False)
items.to_csv(OUT / "order_items.csv", index=False)
payments.to_csv(OUT / "payments.csv", index=False)

print("Sales generation complete.")
print(f"Orders: {len(orders):,}")
print(f"Order items: {len(items):,}")
print(f"Payments: {len(payments):,}")
print(f"Menu price records: {len(prices_df):,}")
print("Sales validations passed.")
