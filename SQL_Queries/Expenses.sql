USE Financial_Operations_DB;
GO

SELECT
    Expense_Category,
    COUNT(*) AS Expense_Count,
    SUM(Expense_Amount) AS Total_Expense,

    CAST(
        SUM(Expense_Amount)
        / NULLIF(
            (SELECT SUM(Expense_Amount) FROM Expenses),
            0
        ) * 100
        AS DECIMAL(10,2)
    ) AS Expense_Percentage

FROM Expenses

GROUP BY
    Expense_Category

ORDER BY
    Total_Expense DESC;