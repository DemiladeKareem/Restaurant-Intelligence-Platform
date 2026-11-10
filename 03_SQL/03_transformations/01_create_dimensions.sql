
USE RestaurantIntelligence;
GO

DROP TABLE IF EXISTS dim.DimBranch;
GO

CREATE TABLE dim.DimBranch (
    BranchID VARCHAR(20) PRIMARY KEY,
    BranchName VARCHAR(150),
    Location VARCHAR(150),
    State VARCHAR(100),
    IsActive BIT
);
GO

INSERT INTO dim.DimBranch (
    BranchID, BranchName, Location, State, IsActive
)
SELECT
    BranchID,
    BranchName,
    Location,
    State,
    CASE
        WHEN LOWER(IsActive) = 'true' THEN 1
        ELSE 0
    END
FROM stg.branches;
GO

DROP TABLE IF EXISTS dim.DimProduct;
GO

CREATE TABLE dim.DimProduct (
    ProductID VARCHAR(20) PRIMARY KEY,
    ProductName VARCHAR(150),
    Category VARCHAR(100),
    BasePriceNGN DECIMAL(18,2),
    StandardUnitCostNGN DECIMAL(18,2),
    SupplyType VARCHAR(50),
    IsActive BIT
);
GO

INSERT INTO dim.DimProduct (
    ProductID,
    ProductName,
    Category,
    BasePriceNGN,
    StandardUnitCostNGN,
    SupplyType,
    IsActive
)
SELECT
    p.ProductID,
    p.ProductName,
    p.Category,
    p.BasePriceNGN,
    c.StandardUnitCostNGN,
    p.SupplyType,
    CASE
        WHEN LOWER(p.IsActive) = 'true' THEN 1
        ELSE 0
    END
FROM stg.menu_products p
LEFT JOIN stg.product_costs c
    ON p.ProductID = c.ProductID;
GO

DROP TABLE IF EXISTS dim.DimFacility;
GO

CREATE TABLE dim.DimFacility (
    FacilityID VARCHAR(20) PRIMARY KEY,
    FacilityName VARCHAR(150),
    FacilityType VARCHAR(50),
    BranchID VARCHAR(20)
);
GO

INSERT INTO dim.DimFacility (
    FacilityID, FacilityName, FacilityType, BranchID
)
SELECT
    FacilityID,
    FacilityName,
    FacilityType,
    NULLIF(BranchID, '')
FROM stg.facilities;
GO

DROP TABLE IF EXISTS dim.DimIngredient;
GO

CREATE TABLE dim.DimIngredient (
    IngredientID VARCHAR(20) PRIMARY KEY,
    IngredientName VARCHAR(150),
    Unit VARCHAR(30),
    StandardCostNGN DECIMAL(18,2)
);
GO

INSERT INTO dim.DimIngredient (
    IngredientID, IngredientName, Unit, StandardCostNGN
)
SELECT
    IngredientID,
    IngredientName,
    Unit,
    StandardCostNGN
FROM stg.ingredients;
GO

DROP TABLE IF EXISTS dim.DimSupplier;
GO

CREATE TABLE dim.DimSupplier (
    SupplierID VARCHAR(20) PRIMARY KEY,
    SupplierName VARCHAR(150)
);
GO

INSERT INTO dim.DimSupplier (
    SupplierID, SupplierName
)
SELECT
    SupplierID,
    SupplierName
FROM stg.suppliers;
GO

SELECT 'DimBranch' AS DimensionName, COUNT(*) AS TotalRows FROM dim.DimBranch
UNION ALL
SELECT 'DimProduct', COUNT(*) FROM dim.DimProduct
UNION ALL
SELECT 'DimFacility', COUNT(*) FROM dim.DimFacility
UNION ALL
SELECT 'DimIngredient', COUNT(*) FROM dim.DimIngredient
UNION ALL
SELECT 'DimSupplier', COUNT(*) FROM dim.DimSupplier;
GO
