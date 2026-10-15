USE Financial_Operations_DB;
GO

SELECT
    YEAR(Invoice_Date) AS Sales_Year,
    MONTH(Invoice_Date) AS Sales_Month,
    DATENAME(MONTH, Invoice_Date) AS Month_Name,
    SUM(Total_Sales_Amount) AS Total_Sales
FROM Sales_Invoices
GROUP BY
    YEAR(Invoice_Date),
    MONTH(Invoice_Date),
    DATENAME(MONTH, Invoice_Date)
ORDER BY
    Sales_Year,
    Sales_Month;