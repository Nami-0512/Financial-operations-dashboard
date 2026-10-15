USE Financial_Operations_DB;
GO

SELECT
    p.Brand,
    SUM(s.Total_Sales_Amount) AS Total_Sales,
    SUM(s.Quantity) AS Total_Quantity,
    COUNT(s.Invoice_ID) AS Total_Invoices
FROM Sales_Invoices s
INNER JOIN Products p
    ON s.Product_ID = p.Product_ID
GROUP BY
    p.Brand
ORDER BY
    Total_Sales DESC;