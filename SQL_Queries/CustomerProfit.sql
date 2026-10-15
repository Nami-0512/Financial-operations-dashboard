USE Financial_Operations_DB;
GO

SELECT TOP 10
    c.Customer_Name,
    SUM(s.Total_Sales_Amount) AS Total_Sales,
    SUM(s.Quantity * p.Cost_Price) AS COGS,
    SUM(s.Total_Sales_Amount)
        - SUM(s.Quantity * p.Cost_Price) AS Gross_Profit,
    CAST(
        (
            SUM(s.Total_Sales_Amount)
            - SUM(s.Quantity * p.Cost_Price)
        ) * 100.0
        / NULLIF(SUM(s.Total_Sales_Amount), 0)
        AS DECIMAL(10,2)
    ) AS Gross_Profit_Margin_Percent
FROM Sales_Invoices s
INNER JOIN Customers c
    ON s.Customer_ID = c.Customer_ID
INNER JOIN Products p
    ON s.Product_ID = p.Product_ID
GROUP BY
    c.Customer_Name
ORDER BY
    Gross_Profit DESC;