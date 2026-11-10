
USE RestaurantIntelligence;
GO

DROP TABLE IF EXISTS stg.branches;
GO
CREATE TABLE stg.branches (
    BranchID VARCHAR(20),
    BranchName VARCHAR(150),
    Location VARCHAR(150),
    State VARCHAR(100),
    IsActive VARCHAR(10)
);
GO

DROP TABLE IF EXISTS stg.facilities;
GO
CREATE TABLE stg.facilities (
    FacilityID VARCHAR(20),
    FacilityName VARCHAR(150),
    FacilityType VARCHAR(50),
    BranchID VARCHAR(20)
);
GO

DROP TABLE IF EXISTS stg.menu_products;
GO
CREATE TABLE stg.menu_products (
    ProductID VARCHAR(20),
    ProductName VARCHAR(150),
    Category VARCHAR(100),
    BasePriceNGN DECIMAL(18,2),
    SupplyType VARCHAR(50),
    IsActive VARCHAR(10)
);
GO

DROP TABLE IF EXISTS stg.product_variants;
GO
CREATE TABLE stg.product_variants (
    VariantID VARCHAR(20),
    ProductID VARCHAR(20),
    VariantName VARCHAR(100),
    SizeMultiplier DECIMAL(18,4)
);
GO

DROP TABLE IF EXISTS stg.ingredients;
GO
CREATE TABLE stg.ingredients (
    IngredientID VARCHAR(20),
    IngredientName VARCHAR(150),
    Unit VARCHAR(30),
    StandardCostNGN DECIMAL(18,2)
);
GO

DROP TABLE IF EXISTS stg.suppliers;
GO
CREATE TABLE stg.suppliers (
    SupplierID VARCHAR(20),
    SupplierName VARCHAR(150)
);
GO

DROP TABLE IF EXISTS stg.stock_locations;
GO
CREATE TABLE stg.stock_locations (
    StockLocationID VARCHAR(20),
    FacilityID VARCHAR(20),
    StockLocationName VARCHAR(150)
);
GO

DROP TABLE IF EXISTS stg.recipes;
GO
CREATE TABLE stg.recipes (
    RecipeID VARCHAR(20),
    ProductID VARCHAR(20),
    YieldPortions INT,
    ProductionFacilityType VARCHAR(50)
);
GO

DROP TABLE IF EXISTS stg.recipe_components;
GO
CREATE TABLE stg.recipe_components (
    RecipeComponentID VARCHAR(30),
    RecipeID VARCHAR(20),
    IngredientID VARCHAR(20),
    QuantityPerPortion DECIMAL(18,6)
);
GO

DROP TABLE IF EXISTS stg.product_costs;
GO
CREATE TABLE stg.product_costs (
    ProductID VARCHAR(20),
    StandardUnitCostNGN DECIMAL(18,2)
);
GO

DROP TABLE IF EXISTS stg.menu_prices;
GO
CREATE TABLE stg.menu_prices (
    PriceID VARCHAR(30),
    BranchID VARCHAR(20),
    ProductID VARCHAR(20),
    VariantID VARCHAR(20),
    PriceMonth VARCHAR(7),
    UnitPriceNGN DECIMAL(18,2)
);
GO

DROP TABLE IF EXISTS stg.orders;
GO
CREATE TABLE stg.orders (
    OrderID VARCHAR(30),
    BranchID VARCHAR(20),
    OrderDate DATE,
    OrderTimestamp DATETIME2,
    SalesChannel VARCHAR(50),
    GrossAmountNGN DECIMAL(18,2),
    DiscountAmountNGN DECIMAL(18,2),
    NetAmountNGN DECIMAL(18,2)
);
GO

DROP TABLE IF EXISTS stg.order_items;
GO
CREATE TABLE stg.order_items (
    OrderItemID VARCHAR(30),
    OrderID VARCHAR(30),
    ProductID VARCHAR(20),
    VariantID VARCHAR(20),
    Quantity INT,
    UnitPriceNGN DECIMAL(18,2),
    GrossAmountNGN DECIMAL(18,2),
    DiscountAmountNGN DECIMAL(18,2),
    NetAmountNGN DECIMAL(18,2)
);
GO

DROP TABLE IF EXISTS stg.payments;
GO
CREATE TABLE stg.payments (
    PaymentID VARCHAR(30),
    OrderID VARCHAR(30),
    PaymentMethod VARCHAR(50),
    PaymentAmountNGN DECIMAL(18,2),
    PaymentStatus VARCHAR(50)
);
GO

DROP TABLE IF EXISTS stg.production_batches;
GO
CREATE TABLE stg.production_batches (
    BatchID VARCHAR(30),
    ProductionDate DATE,
    FacilityID VARCHAR(20),
    BranchID VARCHAR(20),
    ProductID VARCHAR(20),
    ProducedPortions INT,
    SoldPortions INT,
    TransferredPortions INT,
    WastePortions INT,
    RecipeID VARCHAR(20)
);
GO

DROP TABLE IF EXISTS stg.production_consumption;
GO
CREATE TABLE stg.production_consumption (
    ConsumptionID VARCHAR(30),
    BatchID VARCHAR(30),
    ProductionDate DATE,
    FacilityID VARCHAR(20),
    IngredientID VARCHAR(20),
    QuantityConsumed DECIMAL(18,6)
);
GO

DROP TABLE IF EXISTS stg.stock_transfers;
GO
CREATE TABLE stg.stock_transfers (
    TransferID VARCHAR(30),
    TransferDate DATE,
    FromFacilityID VARCHAR(20),
    ToFacilityID VARCHAR(20),
    BranchID VARCHAR(20),
    ProductID VARCHAR(20),
    TransferQuantity INT
);
GO

DROP TABLE IF EXISTS stg.purchase_orders;
GO
CREATE TABLE stg.purchase_orders (
    PurchaseOrderID VARCHAR(30),
    SupplierID VARCHAR(20),
    FacilityID VARCHAR(20),
    PurchaseOrderDate DATE,
    ReceiptDate DATE,
    Status VARCHAR(50)
);
GO

DROP TABLE IF EXISTS stg.purchase_order_lines;
GO
CREATE TABLE stg.purchase_order_lines (
    PurchaseOrderLineID VARCHAR(30),
    PurchaseOrderID VARCHAR(30),
    IngredientID VARCHAR(20),
    OrderQuantity DECIMAL(18,6),
    UnitCostNGN DECIMAL(18,2),
    LineTotalNGN DECIMAL(18,2)
);
GO

DROP TABLE IF EXISTS stg.goods_receipts;
GO
CREATE TABLE stg.goods_receipts (
    GoodsReceiptID VARCHAR(30),
    PurchaseOrderID VARCHAR(30),
    FacilityID VARCHAR(20),
    ReceiptDate DATE
);
GO

DROP TABLE IF EXISTS stg.goods_receipt_lines;
GO
CREATE TABLE stg.goods_receipt_lines (
    GoodsReceiptLineID VARCHAR(30),
    GoodsReceiptID VARCHAR(30),
    IngredientID VARCHAR(20),
    ReceivedQuantity DECIMAL(18,6),
    UnitCostNGN DECIMAL(18,2)
);
GO

DROP TABLE IF EXISTS stg.inventory_movements;
GO
CREATE TABLE stg.inventory_movements (
    MovementID VARCHAR(30),
    MovementDate DATE,
    FacilityID VARCHAR(20),
    StockItemID VARCHAR(20),
    MovementType VARCHAR(60),
    Priority INT,
    QuantityChange DECIMAL(18,6),
    RunningBalance DECIMAL(18,6)
);
GO

DROP TABLE IF EXISTS stg.inventory_reconciliation;
GO
CREATE TABLE stg.inventory_reconciliation (
    FacilityID VARCHAR(20),
    StockItemID VARCHAR(20),
    NetMovement DECIMAL(18,6),
    ClosingBalance DECIMAL(18,6),
    Difference DECIMAL(18,6)
);
GO

DROP TABLE IF EXISTS stg.inventory_stock_exceptions;
GO
CREATE TABLE stg.inventory_stock_exceptions (
    MovementID VARCHAR(30),
    MovementDate DATE,
    FacilityID VARCHAR(20),
    StockItemID VARCHAR(20),
    MovementType VARCHAR(60),
    Priority INT,
    QuantityChange DECIMAL(18,6),
    RunningBalance DECIMAL(18,6)
);
GO

DROP TABLE IF EXISTS stg.operating_expenses;
GO
CREATE TABLE stg.operating_expenses (
    ExpenseID VARCHAR(30),
    BranchID VARCHAR(20),
    ExpenseMonth VARCHAR(7),
    ExpenseCategory VARCHAR(100),
    AmountNGN DECIMAL(18,2)
);
GO

DROP TABLE IF EXISTS stg.monthly_branch_profitability;
GO
CREATE TABLE stg.monthly_branch_profitability (
    BranchID VARCHAR(20),
    Month VARCHAR(7),
    RevenueNGN DECIMAL(18,2),
    StandardCOGSNGN DECIMAL(18,2),
    OperatingExpensesNGN DECIMAL(18,2),
    GrossProfitNGN DECIMAL(18,2),
    EstimatedOperatingProfitNGN DECIMAL(18,2),
    EstimatedOperatingMarginPct DECIMAL(18,4)
);
GO

DROP TABLE IF EXISTS stg.validation_report;
GO
CREATE TABLE stg.validation_report (
    ValidationCheck VARCHAR(200),
    Status VARCHAR(30)
);
GO

SELECT COUNT(*) AS TotalStagingTables
FROM sys.tables
WHERE schema_id = SCHEMA_ID('stg');
