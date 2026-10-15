USE Financial_Operations_DB;
GO

DECLARE @AsOfDate DATE = '2026-03-31';

WITH OutstandingInvoices AS
(
    SELECT
        s.Invoice_ID,
        s.Due_Date,
        s.Total_Sales_Amount - ISNULL(p.Total_Paid, 0) AS Outstanding_Amount
    FROM Sales_Invoices s

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
),

AgingData AS
(
    SELECT
        Outstanding_Amount,

        CASE
            WHEN DATEDIFF(DAY, Due_Date, @AsOfDate) <= 0
                THEN 'Not Due'
            WHEN DATEDIFF(DAY, Due_Date, @AsOfDate) <= 30
                THEN '0-30 Days'
            WHEN DATEDIFF(DAY, Due_Date, @AsOfDate) <= 60
                THEN '31-60 Days'
            WHEN DATEDIFF(DAY, Due_Date, @AsOfDate) <= 90
                THEN '61-90 Days'
            ELSE '90+ Days'
        END AS Aging_Bucket

    FROM OutstandingInvoices
)

SELECT
    Aging_Bucket,
    COUNT(*) AS Invoice_Count,
    SUM(Outstanding_Amount) AS Outstanding_Amount

FROM AgingData

GROUP BY Aging_Bucket

ORDER BY
    CASE Aging_Bucket
        WHEN 'Not Due' THEN 1
        WHEN '0-30 Days' THEN 2
        WHEN '31-60 Days' THEN 3
        WHEN '61-90 Days' THEN 4
        WHEN '90+ Days' THEN 5
    END;