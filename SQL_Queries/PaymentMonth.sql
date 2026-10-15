USE Financial_Operations_DB;
GO

SELECT
    YEAR(Payment_Date) AS Payment_Year,
    MONTH(Payment_Date) AS Payment_Month,
    DATENAME(MONTH, Payment_Date) AS Month_Name,
    SUM(Amount_Paid) AS Total_Collected,
    COUNT(Payment_ID) AS Payment_Count
FROM Payments
GROUP BY
    YEAR(Payment_Date),
    MONTH(Payment_Date),
    DATENAME(MONTH, Payment_Date)
ORDER BY
    Payment_Year,
    Payment_Month;