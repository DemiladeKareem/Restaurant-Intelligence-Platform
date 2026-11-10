
USE RestaurantIntelligence;
GO

SELECT 'branches' AS TableName, COUNT(*) AS TotalRows FROM stg.branches
UNION ALL SELECT 'facilities', COUNT(*) FROM stg.facilities
UNION ALL SELECT 'menu_products', COUNT(*) FROM stg.menu_products
UNION ALL SELECT 'product_variants', COUNT(*) FROM stg.product_variants
UNION ALL SELECT 'ingredients', COUNT(*) FROM stg.ingredients
UNION ALL SELECT 'suppliers', COUNT(*) FROM stg.suppliers
UNION ALL SELECT 'stock_locations', COUNT(*) FROM stg.stock_locations
UNION ALL SELECT 'recipes', COUNT(*) FROM stg.recipes
UNION ALL SELECT 'recipe_components', COUNT(*) FROM stg.recipe_components
UNION ALL SELECT 'product_costs', COUNT(*) FROM stg.product_costs
UNION ALL SELECT 'menu_prices', COUNT(*) FROM stg.menu_prices
UNION ALL SELECT 'orders', COUNT(*) FROM stg.orders
UNION ALL SELECT 'order_items', COUNT(*) FROM stg.order_items
UNION ALL SELECT 'payments', COUNT(*) FROM stg.payments
UNION ALL SELECT 'production_batches', COUNT(*) FROM stg.production_batches
UNION ALL SELECT 'production_consumption', COUNT(*) FROM stg.production_consumption
UNION ALL SELECT 'stock_transfers', COUNT(*) FROM stg.stock_transfers
UNION ALL SELECT 'purchase_orders', COUNT(*) FROM stg.purchase_orders
UNION ALL SELECT 'purchase_order_lines', COUNT(*) FROM stg.purchase_order_lines
UNION ALL SELECT 'goods_receipts', COUNT(*) FROM stg.goods_receipts
UNION ALL SELECT 'goods_receipt_lines', COUNT(*) FROM stg.goods_receipt_lines
UNION ALL SELECT 'inventory_movements', COUNT(*) FROM stg.inventory_movements
UNION ALL SELECT 'inventory_reconciliation', COUNT(*) FROM stg.inventory_reconciliation
UNION ALL SELECT 'inventory_stock_exceptions', COUNT(*) FROM stg.inventory_stock_exceptions
UNION ALL SELECT 'operating_expenses', COUNT(*) FROM stg.operating_expenses
UNION ALL SELECT 'monthly_branch_profitability', COUNT(*) FROM stg.monthly_branch_profitability
UNION ALL SELECT 'validation_report', COUNT(*) FROM stg.validation_report;
GO


SELECT
    COUNT(*) AS TotalBranches,
    SUM(CASE WHEN BranchID IS NULL OR TRIM(BranchID) = '' THEN 1 ELSE 0 END) AS MissingBranchID,
    SUM(CASE WHEN BranchName IS NULL OR TRIM(BranchName) = '' THEN 1 ELSE 0 END) AS MissingBranchName,
    COUNT(*) - COUNT(DISTINCT BranchID) AS DuplicateOrNullBranchIDs
FROM stg.branches;

SELECT
    COUNT(*) AS TotalOrders,
    SUM(CASE WHEN OrderID IS NULL OR TRIM(OrderID) = '' THEN 1 ELSE 0 END) AS MissingOrderID,
    SUM(CASE WHEN BranchID IS NULL OR TRIM(BranchID) = '' THEN 1 ELSE 0 END) AS MissingBranchID,
    SUM(CASE WHEN OrderDate IS NULL THEN 1 ELSE 0 END) AS MissingOrderDate,
    COUNT(*) - COUNT(DISTINCT OrderID) AS DuplicateOrNullOrderIDs
FROM stg.orders;

SELECT
    COUNT(*) AS TotalOrderItems,
    SUM(CASE WHEN OrderItemID IS NULL OR TRIM(OrderItemID) = '' THEN 1 ELSE 0 END) AS MissingOrderItemID,
    SUM(CASE WHEN ProductID IS NULL OR TRIM(ProductID) = '' THEN 1 ELSE 0 END) AS MissingProductID,
    COUNT(*) - COUNT(DISTINCT OrderItemID) AS DuplicateOrNullOrderItemIDs
FROM stg.order_items;
GO



SELECT COUNT(*) AS OrdersWithInvalidBranch
FROM stg.orders o
LEFT JOIN stg.branches b
    ON o.BranchID = b.BranchID
WHERE b.BranchID IS NULL;

SELECT COUNT(*) AS ItemsWithInvalidOrder
FROM stg.order_items oi
LEFT JOIN stg.orders o
    ON oi.OrderID = o.OrderID
WHERE o.OrderID IS NULL;

SELECT COUNT(*) AS ItemsWithInvalidProduct
FROM stg.order_items oi
LEFT JOIN stg.menu_products p
    ON oi.ProductID = p.ProductID
WHERE p.ProductID IS NULL;

SELECT COUNT(*) AS PaymentsWithInvalidOrder
FROM stg.payments p
LEFT JOIN stg.orders o
    ON p.OrderID = o.OrderID
WHERE o.OrderID IS NULL;
GO


SELECT
    SUM(CASE WHEN Quantity <= 0 OR Quantity IS NULL THEN 1 ELSE 0 END) AS InvalidQuantity,
    SUM(CASE WHEN UnitPriceNGN < 0 OR UnitPriceNGN IS NULL THEN 1 ELSE 0 END) AS InvalidUnitPrice,
    SUM(CASE WHEN NetAmountNGN < 0 OR NetAmountNGN IS NULL THEN 1 ELSE 0 END) AS InvalidNetAmount
FROM stg.order_items;

SELECT
    SUM(CASE WHEN NetAmountNGN < 0 OR NetAmountNGN IS NULL THEN 1 ELSE 0 END) AS InvalidOrderNetAmount,
    SUM(CASE WHEN DiscountAmountNGN < 0 OR DiscountAmountNGN IS NULL THEN 1 ELSE 0 END) AS InvalidDiscount,
    SUM(CASE WHEN GrossAmountNGN < NetAmountNGN THEN 1 ELSE 0 END) AS GrossLessThanNet
FROM stg.orders;

SELECT
    MIN(OrderDate) AS FirstOrderDate,
    MAX(OrderDate) AS LastOrderDate,
    COUNT(DISTINCT BranchID) AS ActiveBranchCount
FROM stg.orders;
GO


WITH ItemTotals AS (
    SELECT
        OrderID,
        SUM(NetAmountNGN) AS CalculatedNetAmount
    FROM stg.order_items
    GROUP BY OrderID
)
SELECT
    COUNT(*) AS OrdersChecked,
    SUM(CASE
        WHEN i.OrderID IS NULL
          OR ABS(o.NetAmountNGN - i.CalculatedNetAmount) > 0.01
        THEN 1 ELSE 0
    END) AS OrdersWithMismatch
FROM stg.orders o
LEFT JOIN ItemTotals i
    ON o.OrderID = i.OrderID;
GO



SELECT
    COUNT(*) AS InventoryReconciliationRows,
    SUM(CASE WHEN ABS(Difference) > 0.000001 THEN 1 ELSE 0 END) AS ReconciliationMismatches
FROM stg.inventory_reconciliation;

SELECT
    COUNT(*) AS NegativeStockExceptionRows
FROM stg.inventory_stock_exceptions;

SELECT
    ValidationCheck,
    Status
FROM stg.validation_report;
GO
