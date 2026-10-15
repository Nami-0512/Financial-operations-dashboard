USE Financial_Operations_DB;
GO

SELECT
    YEAR(Expense_Date) AS Expense_Year,
    MONTH(Expense_Date) AS Expense_Month,
    DATENAME(MONTH, Expense_Date) AS Month_Name,
    SUM(Expense_Amount) AS Total_Expenses
FROM Expenses
GROUP BY
    YEAR(Expense_Date),
    MONTH(Expense_Date),
    DATENAME(MONTH, Expense_Date)
ORDER BY
    Expense_Year,
    Expense_Month;