
USE RestaurantIntelligence;
GO

BULK INSERT stg.branches
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\branches.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.facilities
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\facilities.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.menu_products
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\menu_products.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.product_variants
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\product_variants.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.ingredients
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\ingredients.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.suppliers
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\suppliers.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.stock_locations
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\stock_locations.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.recipes
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\recipes.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.recipe_components
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\recipe_components.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.product_costs
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\product_costs.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.menu_prices
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\menu_prices.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.orders
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\orders.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.order_items
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\order_items.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.payments
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\payments.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.production_batches
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\production_batches.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.production_consumption
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\production_consumption.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.stock_transfers
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\stock_transfers.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.purchase_orders
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\purchase_orders.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.purchase_order_lines
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\purchase_order_lines.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.goods_receipts
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\goods_receipts.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.goods_receipt_lines
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\goods_receipt_lines.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.inventory_movements
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\inventory_movements.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.inventory_reconciliation
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\inventory_reconciliation.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.inventory_stock_exceptions
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\inventory_stock_exceptions.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.operating_expenses
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\operating_expenses.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.monthly_branch_profitability
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\monthly_branch_profitability.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO

BULK INSERT stg.validation_report
FROM 'C:\Demilade_Kareem_Projects\Restaurant-Intelligence-Platform\02_Data_Generation\output\validation_report.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, FIELDQUOTE = '"', TABLOCK);
GO


