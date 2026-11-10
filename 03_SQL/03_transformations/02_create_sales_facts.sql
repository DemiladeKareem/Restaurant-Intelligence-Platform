
USE RestaurantIntelligence;
GO

DROP TABLE IF EXISTS facts.FactPayments;
GO

DROP TABLE IF EXISTS facts.FactOrderItems;
GO

DROP TABLE IF EXISTS facts.FactOrders;
GO

CREATE TABLE facts.FactOrders (
    OrderID VARCHAR(30) PRIMARY KEY,
    BranchID VARCHAR(20) NOT NULL,
    OrderDate DATE,
    OrderTimestamp DATETIME2,
    SalesChannel VARCHAR(50),
    GrossAmountNGN DECIMAL(18,2),
    DiscountAmountNGN DECIMAL(18,2),
    NetAmountNGN DECIMAL(18,2),

    FOREIGN KEY (BranchID)
        REFERENCES dim.DimBranch(BranchID)
);
GO

INSERT INTO facts.FactOrders (
    OrderID,
    BranchID,
    OrderDate,
    OrderTimestamp,
    SalesChannel,
    GrossAmountNGN,
    DiscountAmountNGN,
    NetAmountNGN
)
SELECT
    OrderID,
    BranchID,
    OrderDate,
    OrderTimestamp,
    SalesChannel,
    GrossAmountNGN,
    DiscountAmountNGN,
    NetAmountNGN
FROM stg.orders;
GO

CREATE TABLE facts.FactOrderItems (
    OrderItemID VARCHAR(30) PRIMARY KEY,
    OrderID VARCHAR(30) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    VariantID VARCHAR(20),
    Quantity INT,
    UnitPriceNGN DECIMAL(18,2),
    GrossAmountNGN DECIMAL(18,2),
    DiscountAmountNGN DECIMAL(18,2),
    NetAmountNGN DECIMAL(18,2),

    FOREIGN KEY (OrderID)
        REFERENCES facts.FactOrders(OrderID),

    FOREIGN KEY (ProductID)
        REFERENCES dim.DimProduct(ProductID)
);
GO

INSERT INTO facts.FactOrderItems (
    OrderItemID,
    OrderID,
    ProductID,
    VariantID,
    Quantity,
    UnitPriceNGN,
    GrossAmountNGN,
    DiscountAmountNGN,
    NetAmountNGN
)
SELECT
    OrderItemID,
    OrderID,
    ProductID,
    VariantID,
    Quantity,
    UnitPriceNGN,
    GrossAmountNGN,
    DiscountAmountNGN,
    NetAmountNGN
FROM stg.order_items;
GO

CREATE TABLE facts.FactPayments (
    PaymentID VARCHAR(30) PRIMARY KEY,
    OrderID VARCHAR(30) NOT NULL,
    PaymentMethod VARCHAR(50),
    PaymentAmountNGN DECIMAL(18,2),
    PaymentStatus VARCHAR(50),

    FOREIGN KEY (OrderID)
        REFERENCES facts.FactOrders(OrderID)
);
GO

INSERT INTO facts.FactPayments (
    PaymentID,
    OrderID,
    PaymentMethod,
    PaymentAmountNGN,
    PaymentStatus
)
SELECT
    PaymentID,
    OrderID,
    PaymentMethod,
    PaymentAmountNGN,
    PaymentStatus
FROM stg.payments;
GO

SELECT 'FactOrders' AS FactTable, COUNT(*) AS TotalRows
FROM facts.FactOrders

UNION ALL

SELECT 'FactOrderItems', COUNT(*)
FROM facts.FactOrderItems

UNION ALL

SELECT 'FactPayments', COUNT(*)
FROM facts.FactPayments;
GO
