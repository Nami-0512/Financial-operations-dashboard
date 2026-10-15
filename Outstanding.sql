USE Financial_Operations_DB;
GO

SELECT
    s.Invoice_ID,
    s.Invoice_Date,
    s.Due_Date,
    c.Customer_Name,
    s.Total_Sales_Amount AS Invoice_Amount,
    ISNULL(SUM(p.Amount_Paid), 0) AS Amount_Paid,
    s.Total_Sales_Amount - ISNULL(SUM(p.Amount_Paid), 0) AS Outstanding_Amount
FROM Sales_Invoices s
INNER JOIN Customers c
    ON s.Customer_ID = c.Customer_ID
LEFT JOIN Payments p
    ON s.Invoice_ID = p.Invoice_ID
GROUP BY
    s.Invoice_ID,
    s.Invoice_Date,
    s.Due_Date,
    c.Customer_Name,
    s.Total_Sales_Amount
HAVING
    s.Total_Sales_Amount - ISNULL(SUM(p.Amount_Paid), 0) > 0
ORDER BY
    Outstanding_Amount DESC;