
USE RestaurantIntelligence;
GO

DROP TABLE IF EXISTS facts.FactProduction;
GO

CREATE TABLE facts.FactProduction (
    BatchID VARCHAR(30) PRIMARY KEY,
    ProductionDate DATE,
    FacilityID VARCHAR(20),
    BranchID VARCHAR(20),
    ProductID VARCHAR(20),
    ProducedPortions INT,
    SoldPortions INT,
    TransferredPortions INT,
    WastePortions INT,
    RecipeID VARCHAR(20),

    FOREIGN KEY (FacilityID) REFERENCES dim.DimFacility(FacilityID),
    FOREIGN KEY (BranchID) REFERENCES dim.DimBranch(BranchID),
    FOREIGN KEY (ProductID) REFERENCES dim.DimProduct(ProductID)
);
GO

INSERT INTO facts.FactProduction
SELECT
    BatchID, ProductionDate, FacilityID,
    NULLIF(BranchID, ''), ProductID,
    ProducedPortions, SoldPortions,
    TransferredPortions, WastePortions, RecipeID
FROM stg.production_batches;
GO

DROP TABLE IF EXISTS facts.FactProductionConsumption;
GO

CREATE TABLE facts.FactProductionConsumption (
    ConsumptionID VARCHAR(30) PRIMARY KEY,
    BatchID VARCHAR(30),
    ProductionDate DATE,
    FacilityID VARCHAR(20),
    IngredientID VARCHAR(20),
    QuantityConsumed DECIMAL(18,6),

    FOREIGN KEY (BatchID) REFERENCES facts.FactProduction(BatchID),
    FOREIGN KEY (FacilityID) REFERENCES dim.DimFacility(FacilityID),
    FOREIGN KEY (IngredientID) REFERENCES dim.DimIngredient(IngredientID)
);
GO

INSERT INTO facts.FactProductionConsumption
SELECT
    ConsumptionID, BatchID, ProductionDate,
    FacilityID, IngredientID, QuantityConsumed
FROM stg.production_consumption;
GO

DROP TABLE IF EXISTS facts.FactStockTransfers;
GO

CREATE TABLE facts.FactStockTransfers (
    TransferID VARCHAR(30) PRIMARY KEY,
    TransferDate DATE,
    FromFacilityID VARCHAR(20),
    ToFacilityID VARCHAR(20),
    BranchID VARCHAR(20),
    ProductID VARCHAR(20),
    TransferQuantity INT,

    FOREIGN KEY (FromFacilityID) REFERENCES dim.DimFacility(FacilityID),
    FOREIGN KEY (ToFacilityID) REFERENCES dim.DimFacility(FacilityID),
    FOREIGN KEY (BranchID) REFERENCES dim.DimBranch(BranchID),
    FOREIGN KEY (ProductID) REFERENCES dim.DimProduct(ProductID)
);
GO

INSERT INTO facts.FactStockTransfers
SELECT
    TransferID, TransferDate, FromFacilityID,
    ToFacilityID, BranchID, ProductID, TransferQuantity
FROM stg.stock_transfers;
GO

DROP TABLE IF EXISTS facts.FactProcurement;
GO

CREATE TABLE facts.FactProcurement (
    PurchaseOrderLineID VARCHAR(30) PRIMARY KEY,
    PurchaseOrderID VARCHAR(30),
    SupplierID VARCHAR(20),
    FacilityID VARCHAR(20),
    IngredientID VARCHAR(20),
    PurchaseOrderDate DATE,
    ReceiptDate DATE,
    OrderQuantity DECIMAL(18,6),
    UnitCostNGN DECIMAL(18,2),
    LineTotalNGN DECIMAL(18,2),
    Status VARCHAR(50),

    FOREIGN KEY (SupplierID) REFERENCES dim.DimSupplier(SupplierID),
    FOREIGN KEY (FacilityID) REFERENCES dim.DimFacility(FacilityID),
    FOREIGN KEY (IngredientID) REFERENCES dim.DimIngredient(IngredientID)
);
GO

INSERT INTO facts.FactProcurement
SELECT
    l.PurchaseOrderLineID,
    l.PurchaseOrderID,
    p.SupplierID,
    p.FacilityID,
    l.IngredientID,
    p.PurchaseOrderDate,
    p.ReceiptDate,
    l.OrderQuantity,
    l.UnitCostNGN,
    l.LineTotalNGN,
    p.Status
FROM stg.purchase_order_lines l
INNER JOIN stg.purchase_orders p
    ON l.PurchaseOrderID = p.PurchaseOrderID;
GO

DROP TABLE IF EXISTS facts.FactInventory;
GO

CREATE TABLE facts.FactInventory (
    MovementID VARCHAR(30) PRIMARY KEY,
    MovementDate DATE,
    FacilityID VARCHAR(20),
    StockItemID VARCHAR(20),
    MovementType VARCHAR(60),
    Priority INT,
    QuantityChange DECIMAL(18,6),
    RunningBalance DECIMAL(18,6),

    FOREIGN KEY (FacilityID) REFERENCES dim.DimFacility(FacilityID)
);
GO

INSERT INTO facts.FactInventory
SELECT
    MovementID, MovementDate, FacilityID,
    StockItemID, MovementType, Priority,
    QuantityChange, RunningBalance
FROM stg.inventory_movements;
GO

DROP TABLE IF EXISTS facts.FactExpenses;
GO

CREATE TABLE facts.FactExpenses (
    ExpenseID VARCHAR(30) PRIMARY KEY,
    BranchID VARCHAR(20),
    ExpenseMonth VARCHAR(7),
    ExpenseCategory VARCHAR(100),
    AmountNGN DECIMAL(18,2),

    FOREIGN KEY (BranchID) REFERENCES dim.DimBranch(BranchID)
);
GO

INSERT INTO facts.FactExpenses
SELECT
    ExpenseID, BranchID, ExpenseMonth,
    ExpenseCategory, AmountNGN
FROM stg.operating_expenses;
GO

SELECT 'FactProduction' AS FactTable, COUNT(*) AS TotalRows FROM facts.FactProduction
UNION ALL SELECT 'FactProductionConsumption', COUNT(*) FROM facts.FactProductionConsumption
UNION ALL SELECT 'FactStockTransfers', COUNT(*) FROM facts.FactStockTransfers
UNION ALL SELECT 'FactProcurement', COUNT(*) FROM facts.FactProcurement
UNION ALL SELECT 'FactInventory', COUNT(*) FROM facts.FactInventory
UNION ALL SELECT 'FactExpenses', COUNT(*) FROM facts.FactExpenses;
GO
