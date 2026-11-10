
USE RestaurantIntelligence;
GO

CREATE OR ALTER VIEW analytics.vw_FactSales AS
SELECT
    oi.OrderItemID,
    oi.OrderID,
    o.BranchID,
    o.OrderDate,
    o.OrderTimestamp,
    o.SalesChannel,
    oi.ProductID,
    oi.VariantID,
    oi.Quantity,
    oi.UnitPriceNGN,
    oi.GrossAmountNGN,
    oi.DiscountAmountNGN,
    oi.NetAmountNGN,
    CAST(
        oi.Quantity * p.StandardUnitCostNGN
        AS DECIMAL(18,2)
    ) AS EstimatedStandardCOGSNGN,
    CAST(
        oi.NetAmountNGN -
        (oi.Quantity * p.StandardUnitCostNGN)
        AS DECIMAL(18,2)
    ) AS EstimatedGrossProfitNGN
FROM facts.FactOrderItems oi
INNER JOIN facts.FactOrders o
    ON oi.OrderID = o.OrderID
LEFT JOIN dim.DimProduct p
    ON oi.ProductID = p.ProductID;
GO

CREATE OR ALTER VIEW analytics.vw_FactPayments AS
SELECT
    p.PaymentID,
    p.OrderID,
    o.BranchID,
    o.OrderDate,
    p.PaymentMethod,
    p.PaymentStatus,
    p.PaymentAmountNGN
FROM facts.FactPayments p
INNER JOIN facts.FactOrders o
    ON p.OrderID = o.OrderID;
GO

CREATE OR ALTER VIEW analytics.vw_FactProduction AS
SELECT
    p.BatchID,
    p.ProductionDate,
    p.FacilityID,
    p.BranchID,
    p.ProductID,
    p.ProducedPortions,
    p.SoldPortions,
    p.TransferredPortions,
    p.WastePortions,
    CAST(
        p.WastePortions * d.StandardUnitCostNGN
        AS DECIMAL(18,2)
    ) AS EstimatedWasteCostNGN
FROM facts.FactProduction p
LEFT JOIN dim.DimProduct d
    ON p.ProductID = d.ProductID;
GO

CREATE OR ALTER VIEW analytics.vw_FactIngredientConsumption AS
SELECT
    c.ConsumptionID,
    c.BatchID,
    c.ProductionDate,
    c.FacilityID,
    c.IngredientID,
    c.QuantityConsumed,
    i.StandardCostNGN,
    CAST(
        c.QuantityConsumed * i.StandardCostNGN
        AS DECIMAL(18,2)
    ) AS EstimatedConsumptionCostNGN
FROM facts.FactProductionConsumption c
LEFT JOIN dim.DimIngredient i
    ON c.IngredientID = i.IngredientID;
GO

CREATE OR ALTER VIEW analytics.vw_FactProcurement AS
SELECT
    PurchaseOrderLineID,
    PurchaseOrderID,
    SupplierID,
    FacilityID,
    IngredientID,
    PurchaseOrderDate,
    ReceiptDate,
    Status,
    OrderQuantity,
    UnitCostNGN,
    LineTotalNGN
FROM facts.FactProcurement;
GO

CREATE OR ALTER VIEW analytics.vw_FactInventory AS
SELECT
    MovementID,
    MovementDate,
    FacilityID,
    StockItemID,
    MovementType,
    Priority,
    QuantityChange,
    RunningBalance
FROM facts.FactInventory;
GO
