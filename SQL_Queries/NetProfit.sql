USE Financial_Operations_DB;
GO

WITH ProfitData AS
(
    SELECT
        SUM(s.Total_Sales_Amount) AS Total_Sales,
        SUM(s.Quantity * p.Cost_Price) AS COGS
    FROM Sales_Invoices s
    INNER JOIN Products p
        ON s.Product_ID = p.Product_ID
),

ExpenseData AS
(
    SELECT
        SUM(Expense_Amount) AS Total_Expenses
    FROM Expenses
)

SELECT
    pd.Total_Sales,
    pd.COGS,

    pd.Total_Sales - pd.COGS AS Gross_Profit,

    ed.Total_Expenses,

    pd.Total_Sales
        - pd.COGS
        - ed.Total_Expenses AS Net_Profit,

    CAST(
        (
            pd.Total_Sales
            - pd.COGS
            - ed.Total_Expenses
        )
        / NULLIF(pd.Total_Sales, 0) * 100
        AS DECIMAL(10,2)
    ) AS Net_Profit_Margin_Percent

FROM ProfitData pd
CROSS JOIN ExpenseData ed;