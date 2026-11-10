
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"

products = pd.read_csv(OUT / "menu_products.csv")
ingredients = pd.read_csv(OUT / "ingredients.csv")

ingredient_lookup = dict(zip(
    ingredients["IngredientName"],
    ingredients["IngredientID"],
))

# Standard synthetic ingredient quantities per saleable portion.
base_recipes = {
    "Rice": [
        ("Rice", 0.24),
        ("Tomatoes", 0.09),
        ("Onions", 0.025),
        ("Vegetable Oil", 0.025),
        ("Seasoning", 0.008),
    ],
    "Pasta": [
        ("Spaghetti", 0.20),
        ("Tomatoes", 0.09),
        ("Vegetable Oil", 0.025),
        ("Onions", 0.03),
        ("Seasoning", 0.008),
    ],
    "Swallow": [
        ("Garri", 0.25),
        ("Water", 0.30),
    ],
    "Soup": [
        ("Leafy Vegetables", 0.15),
        ("Palm Oil", 0.035),
        ("Pepper", 0.025),
        ("Onions", 0.02),
        ("Seasoning", 0.01),
        ("Fish", 0.08),
    ],
    "Protein": [
        ("Beef", 0.27),
        ("Pepper", 0.025),
        ("Vegetable Oil", 0.02),
        ("Seasoning", 0.008),
    ],
    "Sides": [
        ("Yam", 0.28),
        ("Vegetable Oil", 0.025),
        ("Salt", 0.004),
    ],
    "Bakery": [
        ("Flour", 0.14),
        ("Butter", 0.025),
        ("Sugar", 0.02),
        ("Egg", 0.20),
        ("Milk", 0.025),
        ("Baking Powder", 0.003),
    ],
    "Beverage": [
        ("Hibiscus", 0.025),
        ("Ginger", 0.008),
        ("Sugar", 0.04),
        ("Water", 0.45),
    ],
    "Dessert": [
        ("Fruit Mix", 0.18),
        ("Yoghurt", 0.10),
        ("Sugar", 0.01),
    ],
    "Specials": [
        ("Bread", 0.60),
        ("Chicken", 0.15),
        ("Lettuce", 0.04),
        ("Mayonnaise", 0.025),
        ("Pepper", 0.015),
    ],
}

# Product-level ingredient substitutions.
substitutions = {
    "Fried Rice": {"Tomatoes": "Carrot"},
    "White Rice": {"Tomatoes": "Water"},
    "Rice and Beans": {"Tomatoes": "Beans"},
    "Vegetable Spaghetti": {
        "Tomatoes": "Leafy Vegetables"
    },
    "Stir-Fried Noodles": {"Spaghetti": "Noodles"},
    "Plain Noodles": {"Spaghetti": "Noodles"},
    "Amala": {"Garri": "Yam Flour"},
    "Semo": {"Garri": "Semolina"},
    "Pounded Yam": {"Garri": "Pounded Yam Flour"},
    "Fufu": {"Garri": "Cassava Flour"},
    "Egusi Soup": {"Leafy Vegetables": "Egusi"},
    "Ogbono Soup": {"Leafy Vegetables": "Ogbono"},
    "Gbegiri Soup": {"Leafy Vegetables": "Beans"},
    "Okra Soup": {"Leafy Vegetables": "Okra"},
    "Grilled Chicken": {"Beef": "Chicken"},
    "Grilled Turkey": {"Beef": "Turkey"},
    "Hake Fish": {"Beef": "Fish"},
    "Titus Fish": {"Beef": "Fish"},
    "Goat Meat": {"Beef": "Goat Meat"},
    "Assorted Meat": {"Beef": "Assorted Meat"},
    "Peppered Chicken": {"Beef": "Chicken"},
    "Peppered Turkey": {"Beef": "Turkey"},
    "Fish Stew": {"Beef": "Fish"},
    "Boiled Egg": {"Beef": "Egg"},
    "Fried Egg": {"Beef": "Egg"},
    "Fried Plantain": {"Yam": "Plantain"},
    "Beans Porridge": {"Yam": "Beans"},
    "Potato Fries": {"Yam": "Potato"},
    "Coleslaw": {"Yam": "Cabbage"},
    "Moi Moi": {"Yam": "Beans"},
    "Chicken Pie": {"Sugar": "Chicken"},
    "Sausage Roll": {"Sugar": "Sausage"},
    "Coconut Bread": {"Sugar": "Coconut"},
    "Chocolate Cake Slice": {"Sugar": "Cocoa"},
    "Fish Roll": {"Sugar": "Fish"},
    "Fruit Salad": {"Yoghurt": "Fruit Mix"},
    "Custard Cup": {"Fruit Mix": "Custard Powder"},
    "Beef Shawarma": {"Chicken": "Beef"},
    "Beef Burger": {"Chicken": "Beef"},
    "Grilled Fish Platter": {"Chicken": "Fish"},
}

recipes = []
components = []

for product in products.itertuples(index=False):
    if product.SupplyType == "Purchased":
        continue

    recipe_id = f"REC{len(recipes) + 1:04d}"

    recipes.append({
        "RecipeID": recipe_id,
        "ProductID": product.ProductID,
        "YieldPortions": 1,
        "ProductionFacilityType": product.SupplyType,
    })

    replacements = substitutions.get(
        product.ProductName, {}
    )

    for ingredient_name, quantity in base_recipes[
        product.Category
    ]:
        actual_name = replacements.get(
            ingredient_name, ingredient_name
        )

        if (
            product.ProductName in ("Boiled Egg", "Fried Egg")
            and actual_name == "Egg"
        ):
            quantity = 2

        components.append({
            "RecipeComponentID": (
                f"RC{len(components) + 1:06d}"
            ),
            "RecipeID": recipe_id,
            "IngredientID": ingredient_lookup[actual_name],
            "QuantityPerPortion": quantity,
        })

recipes_df = pd.DataFrame(recipes)
components_df = pd.DataFrame(components)

recipes_df.to_csv(OUT / "recipes.csv", index=False)
components_df.to_csv(
    OUT / "recipe_components.csv", index=False
)

# Calculate standard ingredient cost for every recipe.
cost_details = components_df.merge(
    ingredients[["IngredientID", "StandardCostNGN"]],
    on="IngredientID",
    validate="many_to_one",
)

cost_details["ComponentCostNGN"] = (
    cost_details["QuantityPerPortion"]
    * cost_details["StandardCostNGN"]
)

recipe_costs = (
    cost_details.groupby("RecipeID")["ComponentCostNGN"]
    .sum()
)

recipe_products = recipes_df.set_index("RecipeID")

product_costs = {
    recipe_products.loc[recipe_id, "ProductID"]: round(
        float(cost), 2
    )
    for recipe_id, cost in recipe_costs.items()
}

# Purchased products use their supplier-standard unit cost.
for product in products.itertuples(index=False):
    if product.SupplyType == "Purchased":
        finished_good_id = f"FG{product.ProductID[1:]}"

        matching_cost = ingredients.loc[
            ingredients["IngredientID"] == finished_good_id,
            "StandardCostNGN",
        ]

        product_costs[product.ProductID] = float(
            matching_cost.iloc[0]
        )

costs_df = pd.DataFrame([
    {
        "ProductID": product_id,
        "StandardUnitCostNGN": cost,
    }
    for product_id, cost in product_costs.items()
])

assert len(recipes_df) == 65
assert len(product_costs) == len(products)
assert costs_df["ProductID"].is_unique
assert (costs_df["StandardUnitCostNGN"] > 0).all()

costs_df.to_csv(
    OUT / "product_costs.csv", index=False
)

print(
    f"Recipes complete: {len(recipes_df)} recipes; "
    f"all {len(products)} products have a standard cost."
)
