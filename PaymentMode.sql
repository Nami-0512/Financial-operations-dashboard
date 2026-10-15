USE Financial_Operations_DB;
GO

SELECT
    Payment_Mode,
    COUNT(Payment_ID) AS Payment_Count,
    SUM(Amount_Paid) AS Total_Collected,
    CAST(
        SUM(Amount_Paid) * 100.0
        / NULLIF((SELECT SUM(Amount_Paid) FROM Payments), 0)
        AS DECIMAL(10,2)
    ) AS Collection_Percentage
FROM Payments
GROUP BY Payment_Mode
ORDER BY Total_Collected DESC;