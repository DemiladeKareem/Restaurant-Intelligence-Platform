
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(parents=True, exist_ok=True)

# Five fictional Lagos branches and one central kitchen.
branches = ["Baruwa", "Akowonjo", "Ijegun", "Idimu", "Abule Egba"]

branch_rows = [
    {
        "BranchID": f"BR{i:03d}",
        "BranchName": f"{name} Outlet",
        "Location": name,
        "State": "Lagos",
        "IsActive": True,
    }
    for i, name in enumerate(branches, 1)
]
pd.DataFrame(branch_rows).to_csv(OUT / "branches.csv", index=False)

facility_rows = [
    {
        "FacilityID": f"FAC{i:03d}",
        "FacilityName": f"{name} Kitchen",
        "FacilityType": "Branch Kitchen",
        "BranchID": f"BR{i:03d}",
    }
    for i, name in enumerate(branches, 1)
]
facility_rows.append({
    "FacilityID": "FAC006",
    "FacilityName": "Central Kitchen",
    "FacilityType": "Central Kitchen",
    "BranchID": "",
})
pd.DataFrame(facility_rows).to_csv(
    OUT / "facilities.csv", index=False
)

# All prices and costs are illustrative synthetic NGN values.
menu = [
    ("Jollof Rice", "Rice", 2800, "Branch"),
    ("Fried Rice", "Rice", 3000, "Branch"),
    ("White Rice", "Rice", 2200, "Branch"),
    ("Rice and Beans", "Rice", 2600, "Branch"),
    ("Ofada Rice", "Rice", 3200, "Branch"),

    ("Jollof Spaghetti", "Pasta", 2900, "Branch"),
    ("Vegetable Spaghetti", "Pasta", 2900, "Branch"),
    ("Stir-Fried Noodles", "Pasta", 2600, "Branch"),
    ("Plain Noodles", "Pasta", 2200, "Branch"),

    ("Eba", "Swallow", 1000, "Branch"),
    ("Amala", "Swallow", 1200, "Branch"),
    ("Semo", "Swallow", 1100, "Branch"),
    ("Pounded Yam", "Swallow", 1700, "Branch"),
    ("Fufu", "Swallow", 1100, "Branch"),

    ("Egusi Soup", "Soup", 2400, "Branch"),
    ("Efo Riro", "Soup", 2300, "Branch"),
    ("Ogbono Soup", "Soup", 2500, "Branch"),
    ("Gbegiri Soup", "Soup", 2000, "Branch"),
    ("Okra Soup", "Soup", 2000, "Branch"),
    ("Banga Soup", "Soup", 2700, "Branch"),
    ("Oha Soup", "Soup", 2600, "Branch"),

    ("Fried Beef", "Protein", 2000, "Branch"),
    ("Grilled Chicken", "Protein", 4000, "Branch"),
    ("Grilled Turkey", "Protein", 4500, "Branch"),
    ("Hake Fish", "Protein", 3200, "Branch"),
    ("Titus Fish", "Protein", 2800, "Branch"),
    ("Boiled Egg", "Protein", 700, "Branch"),
    ("Fried Egg", "Protein", 800, "Branch"),
    ("Goat Meat", "Protein", 3400, "Branch"),
    ("Assorted Meat", "Protein", 2500, "Branch"),
    ("Peppered Chicken", "Protein", 4200, "Branch"),
    ("Peppered Turkey", "Protein", 4700, "Branch"),
    ("Fish Stew", "Protein", 3200, "Branch"),
    ("Beef Stew", "Protein", 2400, "Branch"),

    ("Fried Plantain", "Sides", 1200, "Branch"),
    ("Beans Porridge", "Sides", 2300, "Branch"),
    ("Yam Porridge", "Sides", 2500, "Branch"),
    ("Coleslaw", "Sides", 1100, "Branch"),
    ("Moi Moi", "Sides", 1300, "Central"),
    ("Yam Fries", "Sides", 1700, "Branch"),
    ("Potato Fries", "Sides", 1900, "Branch"),

    ("Meat Pie", "Bakery", 1800, "Central"),
    ("Chicken Pie", "Bakery", 2000, "Central"),
    ("Sausage Roll", "Bakery", 1500, "Central"),
    ("Doughnut", "Bakery", 1000, "Central"),
    ("Puff Puff", "Bakery", 800, "Central"),
    ("Bread Loaf", "Bakery", 2500, "Central"),
    ("Coconut Bread", "Bakery", 2800, "Central"),
    ("Chocolate Cake Slice", "Bakery", 2300, "Central"),
    ("Vanilla Cake Slice", "Bakery", 2100, "Central"),
    ("Cupcake", "Bakery", 1400, "Central"),
    ("Chin Chin Pack", "Bakery", 1100, "Central"),
    ("Fish Roll", "Bakery", 1700, "Central"),

    ("Bottled Water", "Beverage", 500, "Purchased"),
    ("Cola", "Beverage", 800, "Purchased"),
    ("Orange Soda", "Beverage", 800, "Purchased"),
    ("Lemon-Lime Soda", "Beverage", 800, "Purchased"),
    ("Malt Drink", "Beverage", 1200, "Purchased"),
    ("Fruit Juice", "Beverage", 1600, "Purchased"),
    ("Yoghurt Drink", "Beverage", 1800, "Purchased"),
    ("Zobo Drink", "Beverage", 1000, "Central"),

    ("Ice Cream Cup", "Dessert", 1700, "Purchased"),
    ("Fruit Salad", "Dessert", 2000, "Central"),
    ("Parfait", "Dessert", 2800, "Central"),
    ("Custard Cup", "Dessert", 1500, "Central"),

    ("Chicken Shawarma", "Specials", 3800, "Branch"),
    ("Beef Shawarma", "Specials", 3500, "Branch"),
    ("Chicken Burger", "Specials", 4000, "Branch"),
    ("Beef Burger", "Specials", 3700, "Branch"),
    ("Club Sandwich", "Specials", 3500, "Branch"),
    ("Pepper Soup", "Specials", 3400, "Branch"),
    ("Grilled Fish Platter", "Specials", 6500, "Branch"),
    ("Breakfast Combo", "Specials", 3500, "Branch"),
]

products = pd.DataFrame([
    {
        "ProductID": f"P{i:03d}",
        "ProductName": name,
        "Category": category,
        "BasePriceNGN": price,
        "SupplyType": supply_type,
        "IsActive": True,
    }
    for i, (name, category, price, supply_type)
    in enumerate(menu, 1)
])
products.to_csv(OUT / "menu_products.csv", index=False)

variants = pd.DataFrame([
    {
        "VariantID": f"V{i:03d}",
        "ProductID": product.ProductID,
        "VariantName": "Standard",
        "SizeMultiplier": 1.0,
    }
    for i, product in enumerate(
        products.itertuples(index=False), 1
    )
])
variants.to_csv(OUT / "product_variants.csv", index=False)

# Ingredient quantities use kg, litres or individual pieces.
ingredients = [
    ("Rice", "kg", 1500),
    ("Beans", "kg", 1700),
    ("Spaghetti", "kg", 2200),
    ("Noodles", "kg", 2800),
    ("Garri", "kg", 950),
    ("Yam Flour", "kg", 2100),
    ("Semolina", "kg", 1800),
    ("Pounded Yam Flour", "kg", 2600),
    ("Cassava Flour", "kg", 1100),
    ("Egusi", "kg", 5500),
    ("Ogbono", "kg", 7200),
    ("Okra", "kg", 1900),
    ("Leafy Vegetables", "kg", 2200),
    ("Tomatoes", "kg", 1900),
    ("Pepper", "kg", 2300),
    ("Onions", "kg", 1600),
    ("Vegetable Oil", "L", 3000),
    ("Palm Oil", "L", 2800),
    ("Seasoning", "kg", 4800),
    ("Salt", "kg", 600),
    ("Chicken", "kg", 5600),
    ("Turkey", "kg", 7200),
    ("Beef", "kg", 5200),
    ("Fish", "kg", 4800),
    ("Goat Meat", "kg", 6800),
    ("Assorted Meat", "kg", 4600),
    ("Egg", "piece", 260),
    ("Plantain", "kg", 1800),
    ("Yam", "kg", 1600),
    ("Potato", "kg", 1700),
    ("Cabbage", "kg", 1800),
    ("Carrot", "kg", 1800),
    ("Flour", "kg", 1500),
    ("Sugar", "kg", 1400),
    ("Butter", "kg", 7500),
    ("Milk", "L", 2400),
    ("Baking Powder", "kg", 5500),
    ("Yeast", "kg", 6800),
    ("Cocoa", "kg", 6500),
    ("Coconut", "kg", 2500),
    ("Sausage", "kg", 4400),
    ("Fruit Mix", "kg", 2600),
    ("Yoghurt", "L", 2600),
    ("Custard Powder", "kg", 2300),
    ("Bread", "piece", 950),
    ("Tortilla", "piece", 650),
    ("Lettuce", "kg", 2500),
    ("Mayonnaise", "kg", 3800),
    ("Hibiscus", "kg", 3400),
    ("Ginger", "kg", 2500),
    ("Spices", "kg", 5500),
    ("Water", "L", 150),
    ("Groundnut Oil", "L", 3100),
]

ingredient_rows = [
    {
        "IngredientID": f"ING{i:03d}",
        "IngredientName": name,
        "Unit": unit,
        "StandardCostNGN": cost,
    }
    for i, (name, unit, cost) in enumerate(ingredients, 1)
]

# Purchased finished goods are tracked as stocked items.
for product in products.itertuples(index=False):
    if product.SupplyType == "Purchased":
        ingredient_rows.append({
            "IngredientID": f"FG{product.ProductID[1:]}",
            "IngredientName": f"Purchased: {product.ProductName}",
            "Unit": "piece",
            "StandardCostNGN": round(
                product.BasePriceNGN * 0.62, 2
            ),
        })

pd.DataFrame(ingredient_rows).to_csv(
    OUT / "ingredients.csv", index=False
)

supplier_names = [
    "Lagos Produce Supply",
    "Mainland Grain Merchants",
    "Fresh Protein Distributors",
    "Bakery Input Traders",
    "Drinks Wholesale Hub",
    "General Food Supply",
]

suppliers = pd.DataFrame([
    {
        "SupplierID": f"SUP{i:03d}",
        "SupplierName": name,
    }
    for i, name in enumerate(supplier_names, 1)
])
suppliers.to_csv(OUT / "suppliers.csv", index=False)

stock_locations = pd.DataFrame([
    {
        "StockLocationID": f"ST{i:03d}",
        "FacilityID": f"FAC{i:03d}",
        "StockLocationName": "Main Store",
    }
    for i in range(1, 7)
])
stock_locations.to_csv(
    OUT / "stock_locations.csv", index=False
)

assert products.ProductID.is_unique
assert variants.VariantID.is_unique
assert len(products) == 73
assert len(branch_rows) == 5

print(
    f"Reference data complete: {len(products)} products, "
    f"{len(ingredient_rows)} stocked items, "
    "5 branches + central kitchen."
)
