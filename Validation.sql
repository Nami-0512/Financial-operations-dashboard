USE Financial_Operations_DB;
GO

SELECT 'Customers' AS Table_Name, COUNT(*) AS Row_Count FROM Customers
UNION ALL
SELECT 'Products', COUNT(*) FROM Products
UNION ALL
SELECT 'Purchases', COUNT(*) FROM Purchases
UNION ALL
SELECT 'Sales_Invoices', COUNT(*) FROM Sales_Invoices
UNION ALL
SELECT 'Payments', COUNT(*) FROM Payments
UNION ALL
SELECT 'Expenses', COUNT(*) FROM Expenses;

USE Financial_Operations_DB;
GO

SELECT
    COUNT(*) AS Total_Invoices,
    SUM(Total_Sales_Amount) AS Total_Sales
FROM Sales_Invoices;

SELECT
    COUNT(*) AS Total_Payments,
    SUM(Amount_Paid) AS Total_Collected
FROM Payments;

SELECT
    COUNT(*) AS Total_Purchases,
    SUM(Total_Purchase_Amount) AS Total_Purchase_Value
FROM Purchases;

SELECT
    COUNT(*) AS Total_Expenses,
    SUM(Expense_Amount) AS Total_Expenses
FROM Expenses;