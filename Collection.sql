USE Financial_Operations_DB;
GO

SELECT
    SUM(s.Total_Sales_Amount) AS Total_Invoice_Value,
    ISNULL(SUM(p.Total_Paid), 0) AS Total_Collected,
    SUM(s.Total_Sales_Amount) - ISNULL(SUM(p.Total_Paid), 0) AS Total_Outstanding,
    CAST(
        ISNULL(SUM(p.Total_Paid), 0) * 100.0
        / NULLIF(SUM(s.Total_Sales_Amount), 0)
        AS DECIMAL(10,2)
    ) AS Collection_Rate_Percent
FROM Sales_Invoices s
LEFT JOIN
(
    SELECT
        Invoice_ID,
        SUM(Amount_Paid) AS Total_Paid
    FROM Payments
    GROUP BY Invoice_ID
) p
    ON s.Invoice_ID = p.Invoice_ID;