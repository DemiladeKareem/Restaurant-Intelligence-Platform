
USE master;
GO

IF DB_ID('RestaurantIntelligence') IS NULL
BEGIN
    CREATE DATABASE RestaurantIntelligence;
END;
GO

USE RestaurantIntelligence;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.schemas WHERE name = 'stg'
)
    EXEC('CREATE SCHEMA stg');
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.schemas WHERE name = 'dim'
)
    EXEC('CREATE SCHEMA dim');
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.schemas WHERE name = 'facts'
)
    EXEC('CREATE SCHEMA facts');
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.schemas WHERE name = 'analytics'
)
    EXEC('CREATE SCHEMA analytics');
GO

SELECT
    DB_NAME() AS CurrentDatabase,
    name AS SchemaName
FROM sys.schemas
WHERE name IN ('stg', 'dim', 'facts', 'analytics');
