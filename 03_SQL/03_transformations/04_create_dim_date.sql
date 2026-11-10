USE RestaurantIntelligence;
GO

DROP TABLE IF EXISTS dim.DimDate;
GO

CREATE TABLE dim.DimDate (
    Date DATE PRIMARY KEY,
    Year INT,
    Quarter INT,
    MonthNumber INT,
    MonthName VARCHAR(20),
    YearMonth VARCHAR(7),
    DayOfMonth INT,
    DayName VARCHAR(20),
    DayOfWeek INT,
    IsWeekend BIT
);
GO

DECLARE @StartDate DATE;
DECLARE @EndDate DATE;

SELECT
    @StartDate = MIN(OrderDate),
    @EndDate = MAX(OrderDate)
FROM facts.FactOrders;

WITH DateSeries AS (
    SELECT @StartDate AS Date

    UNION ALL

    SELECT DATEADD(DAY, 1, Date)
    FROM DateSeries
    WHERE Date < @EndDate
)

INSERT INTO dim.DimDate (
    Date,
    Year,
    Quarter,
    MonthNumber,
    MonthName,
    YearMonth,
    DayOfMonth,
    DayName,
    DayOfWeek,
    IsWeekend
)

SELECT
    Date,
    YEAR(Date),
    DATEPART(QUARTER, Date),
    MONTH(Date),
    DATENAME(MONTH, Date),
    CONVERT(VARCHAR(7), Date, 126),
    DAY(Date),
    DATENAME(WEEKDAY, Date),
    DATEPART(WEEKDAY, Date),

    CASE
        WHEN DATENAME(WEEKDAY, Date) IN ('Saturday', 'Sunday')
        THEN 1
        ELSE 0
    END

FROM DateSeries
OPTION (MAXRECURSION 0);
GO

SELECT
    MIN(Date) AS StartDate,
    MAX(Date) AS EndDate,
    COUNT(*) AS TotalDays
FROM dim.DimDate;
GO