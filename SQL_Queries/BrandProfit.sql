USE Financial_Operations_DB;
GO

SELECT
    p.Brand,

    SUM(s.Total_Sales_Amount) AS Total_Sales,

    SUM(s.Quantity * p.Cost_Price) AS COGS,

    SUM(s.Total_Sales_Amount)
        - SUM(s.Quantity * p.Cost_Price) AS Gross_Profit,

    CAST(
        (
            SUM(s.Total_Sales_Amount)
            - SUM(s.Quantity * p.Cost_Price)
        ) / NULLIF(SUM(s.Total_Sales_Amount), 0) * 100
        AS DECIMAL(10,2)
    ) AS Gross_Profit_Margin_Percent

FROM Sales_Invoices s

INNER JOIN Products p
    ON s.Product_ID = p.Product_ID

GROUP BY
    p.Brand

ORDER BY
    Gross_Profit DESC;