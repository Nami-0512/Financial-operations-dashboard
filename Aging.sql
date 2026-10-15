USE Financial_Operations_DB;
GO

DECLARE @AsOfDate DATE = '2026-03-31';

SELECT
    s.Invoice_ID,
    s.Invoice_Date,
    s.Due_Date,
    c.Customer_Name,
    s.Total_Sales_Amount AS Invoice_Amount,
    ISNULL(p.Total_Paid, 0) AS Amount_Paid,

    s.Total_Sales_Amount - ISNULL(p.Total_Paid, 0) AS Outstanding_Amount,

    DATEDIFF(DAY, s.Due_Date, @AsOfDate) AS Days_Overdue,

    CASE
        WHEN DATEDIFF(DAY, s.Due_Date, @AsOfDate) <= 0
            THEN 'Not Due'
        WHEN DATEDIFF(DAY, s.Due_Date, @AsOfDate) <= 30
            THEN '0-30 Days'
        WHEN DATEDIFF(DAY, s.Due_Date, @AsOfDate) <= 60
            THEN '31-60 Days'
        WHEN DATEDIFF(DAY, s.Due_Date, @AsOfDate) <= 90
            THEN '61-90 Days'
        ELSE '90+ Days'
    END AS Aging_Bucket

FROM Sales_Invoices s

INNER JOIN Customers c
    ON s.Customer_ID = c.Customer_ID

LEFT JOIN
(
    SELECT
        Invoice_ID,
        SUM(Amount_Paid) AS Total_Paid
    FROM Payments
    GROUP BY Invoice_ID
) p
    ON s.Invoice_ID = p.Invoice_ID

WHERE
    s.Total_Sales_Amount - ISNULL(p.Total_Paid, 0) > 0

ORDER BY
    Outstanding_Amount DESC;