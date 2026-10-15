import pandas as pd
from pathlib import Path

print("Financial Operations Dashboard - Python Analysis")

# Project folder
project_folder = Path(__file__).resolve().parent.parent

# Main transaction workbook
excel_file = project_folder / "Excel_Data" / "Financial_Operations_Dashboard_Data_FY2025_26.xlsx"

# Load all tables
customers = pd.read_excel(excel_file, sheet_name="Customers")
products = pd.read_excel(excel_file, sheet_name="Products")
sales = pd.read_excel(excel_file, sheet_name="Sales_Invoices")
purchases = pd.read_excel(excel_file, sheet_name="Purchases")
payments = pd.read_excel(excel_file, sheet_name="Payments")
expenses = pd.read_excel(excel_file, sheet_name="Expenses")

print("\nData loaded successfully!")

print("\nCustomers:", customers.shape)
print("Products:", products.shape)
print("Sales:", sales.shape)
print("Purchases:", purchases.shape)
print("Payments:", payments.shape)
print("Expenses:", expenses.shape)

# ==========================================
# 1. FINANCIAL KPI ANALYSIS
# ==========================================

total_sales = sales["Total_Sales_Amount"].sum()
total_purchases = purchases["Total_Purchase_Amount"].sum()
total_collected = payments["Amount_Paid"].sum()
total_expenses = expenses["Expense_Amount"].sum()

# COGS = quantity sold × product cost price
sales_with_cost = sales.merge(
    products[["Product_ID", "Cost_Price"]],
    on="Product_ID",
    how="left"
)

sales_with_cost["COGS"] = (
    sales_with_cost["Quantity"] *
    sales_with_cost["Cost_Price"]
)

total_cogs = sales_with_cost["COGS"].sum()

gross_profit = total_sales - total_cogs
gross_profit_margin = (gross_profit / total_sales) * 100

net_profit = gross_profit - total_expenses
net_profit_margin = (net_profit / total_sales) * 100

total_outstanding = total_sales - total_collected
collection_rate = (total_collected / total_sales) * 100

print("\n==========================================")
print("FINANCIAL KPI ANALYSIS")
print("==========================================")

print(f"Total Sales       : ₹{total_sales:,.2f}")
print(f"Total Purchases   : ₹{total_purchases:,.2f}")
print(f"Total Collected   : ₹{total_collected:,.2f}")
print(f"Outstanding       : ₹{total_outstanding:,.2f}")
print(f"Total COGS        : ₹{total_cogs:,.2f}")
print(f"Gross Profit      : ₹{gross_profit:,.2f}")
print(f"Gross Margin      : {gross_profit_margin:.2f}%")
print(f"Total Expenses    : ₹{total_expenses:,.2f}")
print(f"Net Profit        : ₹{net_profit:,.2f}")
print(f"Net Margin        : {net_profit_margin:.2f}%")
print(f"Collection Rate   : {collection_rate:.2f}%")


# ==========================================
# 2. MONTHLY SALES ANALYSIS
# ==========================================

sales["Invoice_Date"] = pd.to_datetime(sales["Invoice_Date"])

sales["FY_Month"] = sales["Invoice_Date"].dt.to_period("M")

monthly_sales = (
    sales.groupby("FY_Month")["Total_Sales_Amount"]
    .sum()
    .reset_index()
)

monthly_sales["Month_Name"] = (
    monthly_sales["FY_Month"]
    .dt.strftime("%b %Y")
)

print("\n==========================================")
print("MONTHLY SALES ANALYSIS")
print("==========================================")

print(monthly_sales.to_string(index=False))

# Highest sales month
best_month = monthly_sales.loc[
    monthly_sales["Total_Sales_Amount"].idxmax()
]

print("\nHighest Sales Month:")
print(
    best_month["Month_Name"],
    "₹{:,.2f}".format(best_month["Total_Sales_Amount"])
)



# ==========================================
# 3. BRAND-WISE PROFITABILITY
# ==========================================

brand_data = sales.merge(
    products[["Product_ID", "Brand", "Cost_Price"]],
    on="Product_ID",
    how="left"
)

brand_data["COGS"] = (
    brand_data["Quantity"] *
    brand_data["Cost_Price"]
)

brand_profit = (
    brand_data
    .groupby("Brand")
    .agg(
        Total_Sales=("Total_Sales_Amount", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Invoice_Count=("Invoice_ID", "count"),
        COGS=("COGS", "sum")
    )
    .reset_index()
)

brand_profit["Gross_Profit"] = (
    brand_profit["Total_Sales"] -
    brand_profit["COGS"]
)

brand_profit["Gross_Profit_Margin"] = (
    brand_profit["Gross_Profit"] /
    brand_profit["Total_Sales"]
) * 100

brand_profit = brand_profit.sort_values(
    "Gross_Profit",
    ascending=False
)

print("\n==========================================")
print("BRAND-WISE PROFITABILITY")
print("==========================================")

print(
    brand_profit.to_string(
        index=False,
        formatters={
            "Total_Sales": "₹{:,.2f}".format,
            "COGS": "₹{:,.2f}".format,
            "Gross_Profit": "₹{:,.2f}".format,
            "Gross_Profit_Margin": "{:.2f}%".format
        }
    )
)



# ==========================================
# 4. CUSTOMER-WISE PROFITABILITY
# ==========================================

customer_data = sales.merge(
    products[["Product_ID", "Cost_Price"]],
    on="Product_ID",
    how="left"
)

customer_data["COGS"] = (
    customer_data["Quantity"] *
    customer_data["Cost_Price"]
)

customer_profit = (
    customer_data
    .groupby("Customer_ID")
    .agg(
        Total_Sales=("Total_Sales_Amount", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Invoice_Count=("Invoice_ID", "count"),
        COGS=("COGS", "sum")
    )
    .reset_index()
)

customer_profit = customer_profit.merge(
    customers[["Customer_ID", "Customer_Name"]],
    on="Customer_ID",
    how="left"
)

customer_profit["Gross_Profit"] = (
    customer_profit["Total_Sales"] -
    customer_profit["COGS"]
)

customer_profit["Gross_Profit_Margin"] = (
    customer_profit["Gross_Profit"] /
    customer_profit["Total_Sales"]
) * 100

customer_profit = customer_profit.sort_values(
    "Gross_Profit",
    ascending=False
)

print("\n==========================================")
print("TOP 10 CUSTOMERS BY PROFIT")
print("==========================================")

print(
    customer_profit[
        [
            "Customer_Name",
            "Total_Sales",
            "Total_Quantity",
            "Invoice_Count",
            "COGS",
            "Gross_Profit",
            "Gross_Profit_Margin"
        ]
    ].head(10).to_string(
        index=False,
        formatters={
            "Total_Sales": "₹{:,.2f}".format,
            "COGS": "₹{:,.2f}".format,
            "Gross_Profit": "₹{:,.2f}".format,
            "Gross_Profit_Margin": "{:.2f}%".format
        }
    )
)


# ==========================================
# 5. ACCOUNTS RECEIVABLE AGING ANALYSIS
# ==========================================

from datetime import datetime

# Calculate total payment received per invoice
payment_summary = (
    payments
    .groupby("Invoice_ID")["Amount_Paid"]
    .sum()
    .reset_index()
)

# Merge payments with sales invoices
aging_data = sales.merge(
    payment_summary,
    on="Invoice_ID",
    how="left"
)

aging_data["Amount_Paid"] = aging_data["Amount_Paid"].fillna(0)

# Outstanding amount
aging_data["Outstanding_Amount"] = (
    aging_data["Total_Sales_Amount"] -
    aging_data["Amount_Paid"]
)

# Calculate aging days
today = aging_data["Invoice_Date"].max()

aging_data["Aging_Days"] = (
    today - aging_data["Due_Date"]
).dt.days

# Only outstanding invoices should be considered for AR aging
aging_data["Aging_Days"] = aging_data["Aging_Days"].clip(lower=0)

# Aging buckets
def aging_bucket(days):
    if days <= 30:
        return "0-30 Days"
    elif days <= 60:
        return "31-60 Days"
    elif days <= 90:
        return "61-90 Days"
    else:
        return "90+ Days"

aging_data["Aging_Bucket"] = (
    aging_data["Aging_Days"]
    .apply(aging_bucket)
)

# Customer name
aging_data = aging_data.merge(
    customers[["Customer_ID", "Customer_Name"]],
    on="Customer_ID",
    how="left"
)

# Keep only outstanding invoices
outstanding = aging_data[
    aging_data["Outstanding_Amount"] > 0
].copy()

# Sort highest outstanding first
outstanding = outstanding.sort_values(
    "Outstanding_Amount",
    ascending=False
)

print("\n==========================================")
print("ACCOUNTS RECEIVABLE AGING ANALYSIS")
print("==========================================")

print(
    outstanding[
        [
            "Invoice_ID",
            "Customer_Name",
            "Invoice_Date",
            "Due_Date",
            "Total_Sales_Amount",
            "Amount_Paid",
            "Outstanding_Amount",
            "Aging_Days",
            "Aging_Bucket"
        ]
    ].head(15).to_string(
        index=False,
        formatters={
            "Total_Sales_Amount": "₹{:,.2f}".format,
            "Amount_Paid": "₹{:,.2f}".format,
            "Outstanding_Amount": "₹{:,.2f}".format
        }
    )
)

print("\nOutstanding by Aging Bucket:")

aging_summary = (
    outstanding
    .groupby("Aging_Bucket")["Outstanding_Amount"]
    .sum()
    .reindex(
        ["0-30 Days", "31-60 Days", "61-90 Days", "90+ Days"]
    )
    .fillna(0)
)

print("\nOutstanding by Aging Bucket:")

for bucket, amount in aging_summary.items():
    print(f"{bucket:<12} ₹{amount:,.2f}")


# ==========================================
# 6. EXPENSE ANALYSIS
# ==========================================

expense_summary = (
    expenses
    .groupby("Expense_Category")
    .agg(
        Total_Expense=("Expense_Amount", "sum"),
        Transaction_Count=("Expense_ID", "count")
    )
    .reset_index()
)

expense_summary["Expense_Percentage"] = (
    expense_summary["Total_Expense"] /
    expense_summary["Total_Expense"].sum()
) * 100

expense_summary = expense_summary.sort_values(
    "Total_Expense",
    ascending=False
)

print("\n==========================================")
print("EXPENSE ANALYSIS")
print("==========================================")

print(
    expense_summary.to_string(
        index=False,
        formatters={
            "Total_Expense": "₹{:,.2f}".format,
            "Expense_Percentage": "{:.2f}%".format
        }
    )
)

highest_expense = expense_summary.iloc[0]

print("\nHighest Expense Category:")
print(
    f"{highest_expense['Expense_Category']} "
    f"₹{highest_expense['Total_Expense']:,.2f}"
)


# ==========================================
# 7. PAYMENT ANALYSIS
# ==========================================

payment_summary = (
    payments
    .groupby("Payment_Mode")
    .agg(
        Total_Collected=("Amount_Paid", "sum"),
        Payment_Count=("Payment_ID", "count")
    )
    .reset_index()
)

payment_summary["Collection_Percentage"] = (
    payment_summary["Total_Collected"] /
    payment_summary["Total_Collected"].sum()
) * 100

payment_summary = payment_summary.sort_values(
    "Total_Collected",
    ascending=False
)

print("\n==========================================")
print("PAYMENT ANALYSIS")
print("==========================================")

print(
    payment_summary.to_string(
        index=False,
        formatters={
            "Total_Collected": "₹{:,.2f}".format,
            "Collection_Percentage": "{:.2f}%".format
        }
    )
)

top_payment_mode = payment_summary.iloc[0]

print("\nHighest Collection Payment Mode:")
print(
    f"{top_payment_mode['Payment_Mode']} "
    f"₹{top_payment_mode['Total_Collected']:,.2f}"
)


# ==========================================
# 8. MONTHLY PAYMENT ANALYSIS
# ==========================================

payments["Payment_Date"] = pd.to_datetime(payments["Payment_Date"])

monthly_payments = (
    payments
    .groupby(payments["Payment_Date"].dt.to_period("M"))
    .agg(
        Total_Collected=("Amount_Paid", "sum"),
        Payment_Count=("Payment_ID", "count")
    )
    .reset_index()
)

monthly_payments["FY_Month"] = monthly_payments["Payment_Date"].astype(str)

monthly_payments["Month_Name"] = (
    monthly_payments["Payment_Date"]
    .dt.strftime("%b %Y")
)

monthly_payments = monthly_payments.sort_values("Payment_Date")

print("\n==========================================")
print("MONTHLY PAYMENT ANALYSIS")
print("==========================================")

print(
    monthly_payments[
        ["FY_Month", "Total_Collected", "Payment_Count", "Month_Name"]
    ].to_string(
        index=False,
        formatters={
            "Total_Collected": "₹{:,.2f}".format
        }
    )
)

highest_collection_month = monthly_payments.loc[
    monthly_payments["Total_Collected"].idxmax()
]

print("\nHighest Collection Month:")
print(
    f"{highest_collection_month['Month_Name']} "
    f"₹{highest_collection_month['Total_Collected']:,.2f}"
)

# ==========================================
# 9. CUSTOMER OUTSTANDING ANALYSIS
# ==========================================

# Calculate total payments received for each invoice
payment_totals = (
    payments
    .groupby("Invoice_ID", as_index=False)["Amount_Paid"]
    .sum()
    .rename(columns={"Amount_Paid": "Amount_Paid"})
)

# Merge sales with customer names
aging = sales.merge(
    customers[["Customer_ID", "Customer_Name"]],
    on="Customer_ID",
    how="left"
)

# Merge total payments received
aging = aging.merge(
    payment_totals,
    on="Invoice_ID",
    how="left"
)

# Invoices without payments = ₹0 paid
aging["Amount_Paid"] = aging["Amount_Paid"].fillna(0)

# Calculate outstanding amount
aging["Outstanding_Amount"] = (
    aging["Total_Sales_Amount"] -
    aging["Amount_Paid"]
)

# Keep only invoices with outstanding balance
aging = aging[
    aging["Outstanding_Amount"] > 0
].copy()

# Customer-wise outstanding analysis
customer_outstanding = (
    aging
    .groupby("Customer_Name")
    .agg(
        Total_Sales=("Total_Sales_Amount", "sum"),
        Total_Paid=("Amount_Paid", "sum"),
        Outstanding=("Outstanding_Amount", "sum"),
        Invoice_Count=("Invoice_ID", "count")
    )
    .reset_index()
)

customer_outstanding = customer_outstanding.sort_values(
    "Outstanding",
    ascending=False
).head(10)

print("\n==========================================")
print("TOP 10 CUSTOMERS BY OUTSTANDING")
print("==========================================")

print(
    customer_outstanding.to_string(
        index=False,
        formatters={
            "Total_Sales": "₹{:,.2f}".format,
            "Total_Paid": "₹{:,.2f}".format,
            "Outstanding": "₹{:,.2f}".format
        }
    )
)



# ==========================================
# 10. CUSTOMER COLLECTION RATE ANALYSIS
# ==========================================

customer_collection = (
    aging
    .groupby("Customer_Name")
    .agg(
        Total_Sales=("Total_Sales_Amount", "sum"),
        Total_Paid=("Amount_Paid", "sum"),
        Outstanding=("Outstanding_Amount", "sum")
    )
    .reset_index()
)

customer_collection["Collection_Rate"] = (
    customer_collection["Total_Paid"] /
    customer_collection["Total_Sales"]
) * 100

customer_collection = customer_collection.sort_values(
    "Collection_Rate",
    ascending=False
)

print("\n==========================================")
print("CUSTOMER COLLECTION RATE ANALYSIS")
print("==========================================")

print(
    customer_collection.head(10).to_string(
        index=False,
        formatters={
            "Total_Sales": "₹{:,.2f}".format,
            "Total_Paid": "₹{:,.2f}".format,
            "Outstanding": "₹{:,.2f}".format,
            "Collection_Rate": "{:.2f}%".format
        }
    )
)




# ==========================================
# 11. PYTHON VISUALIZATIONS
# CHART 1 - MONTHLY SALES TREND
# ==========================================

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["Month_Name"],
    monthly_sales["Total_Sales_Amount"],
    marker="o"
)

plt.title("Monthly Sales Trend - FY 2025-26")
plt.xlabel("Month")
plt.ylabel("Sales Amount (₹)")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.show()



# ============================================
# CHART 2 - BRAND-WISE PROFITABILITY
# ============================================

# Create brand profitability data for visualization
brand_chart = sales.merge(
    products[["Product_ID", "Brand", "Cost_Price"]],
    on="Product_ID",
    how="left"
)

brand_chart["COGS"] = (
    brand_chart["Quantity"] *
    brand_chart["Cost_Price"]
)

brand_chart["Gross_Profit"] = (
    brand_chart["Total_Sales_Amount"] -
    brand_chart["COGS"]
)

brand_profitability_chart = (
    brand_chart
    .groupby("Brand", as_index=False)
    .agg(
        Total_Sales=("Total_Sales_Amount", "sum"),
        COGS=("COGS", "sum"),
        Gross_Profit=("Gross_Profit", "sum")
    )
)

# Create chart
plt.figure(figsize=(10, 6))

plt.bar(
    brand_profitability_chart["Brand"],
    brand_profitability_chart["Gross_Profit"]
)

plt.title("Brand-wise Gross Profit - FY 2025-26")
plt.xlabel("Brand")
plt.ylabel("Gross Profit (₹)")

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================
# CHART 3 - OUTSTANDING BY AGING BUCKET
# ============================================

aging_chart = (
    aging_summary
    .reset_index()
)

aging_chart.columns = ["Aging_Bucket", "Outstanding"]

plt.figure(figsize=(10, 6))

plt.bar(
    aging_chart["Aging_Bucket"],
    aging_chart["Outstanding"]
)

plt.title("Outstanding by Aging Bucket - FY 2025-26")
plt.xlabel("Aging Bucket")
plt.ylabel("Outstanding Amount (₹)")

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================
# CHART 4 - EXPENSE DISTRIBUTION
# ============================================

expense_chart = (
    expenses.groupby("Expense_Category", as_index=False)
    ["Expense_Amount"]
    .sum()
    .sort_values("Expense_Amount", ascending=False)
)

plt.figure(figsize=(10, 6))

plt.bar(
    expense_chart["Expense_Category"],
    expense_chart["Expense_Amount"]
)

plt.title("Expense Distribution by Category - FY 2025-26")
plt.xlabel("Expense Category")
plt.ylabel("Expense Amount (₹)")

plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================
# CHART 5 - MONTHLY COLLECTIONS
# ============================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_payments["Month_Name"],
    monthly_payments["Total_Collected"],
    marker="o"
)

plt.title("Monthly Collections Trend - FY 2025-26")
plt.xlabel("Month")
plt.ylabel("Amount Collected (₹)")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================
# CHART 6 - TOP 10 CUSTOMERS BY OUTSTANDING
# ============================================

customer_outstanding_chart = (
    customer_outstanding
    .sort_values("Outstanding", ascending=False)
    .head(10)
    .sort_values("Outstanding", ascending=True)
)

plt.figure(figsize=(10, 6))

plt.barh(
    customer_outstanding_chart["Customer_Name"],
    customer_outstanding_chart["Outstanding"]
)

plt.title("Top 10 Customers by Outstanding - FY 2025-26")
plt.xlabel("Outstanding Amount (₹)")
plt.ylabel("Customer")

plt.grid(axis="x", alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================
# CHART 7 - CUSTOMER PROFITABILITY ANALYSIS
# ============================================================

customer_profitability = (
    sales
    .merge(
        products[["Product_ID", "Cost_Price"]],
        on="Product_ID",
        how="left"
    )
    .merge(
        customers[["Customer_ID", "Customer_Name"]],
        on="Customer_ID",
        how="left"
    )
)

# Calculate COGS
customer_profitability["COGS"] = (
    customer_profitability["Quantity"]
    * customer_profitability["Cost_Price"]
)

# Customer-level profitability
customer_profit = (
    customer_profitability
    .groupby("Customer_Name")
    .agg(
        Total_Sales=("Total_Sales_Amount", "sum"),
        COGS=("COGS", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .reset_index()
)

# Gross Profit
customer_profit["Gross_Profit"] = (
    customer_profit["Total_Sales"]
    - customer_profit["COGS"]
)

# Gross Profit Margin
customer_profit["Gross_Profit_Margin"] = (
    customer_profit["Gross_Profit"]
    / customer_profit["Total_Sales"]
    * 100
)

# Display top 10 customers by Gross Profit
top_customer_profit = (
    customer_profit
    .sort_values("Gross_Profit", ascending=False)
    .head(10)
    .sort_values("Gross_Profit", ascending=True)
)

print("\n" + "=" * 70)
print("TOP 10 CUSTOMERS BY GROSS PROFIT")
print("=" * 70)

print(
    top_customer_profit[
        [
            "Customer_Name",
            "Total_Sales",
            "COGS",
            "Gross_Profit",
            "Gross_Profit_Margin"
        ]
    ].to_string(index=False)
)

# Chart
plt.figure(figsize=(10, 6))

plt.barh(
    top_customer_profit["Customer_Name"],
    top_customer_profit["Gross_Profit"]
)

plt.title("Top 10 Customers by Gross Profit - FY 2025-26")
plt.xlabel("Gross Profit (₹)")
plt.ylabel("Customer")

plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# ============================================================
# CHART 8 - MONTHLY NET PROFIT ANALYSIS
# ============================================================

# Monthly Gross Profit from sales
monthly_gross_profit = (
    sales_with_cost
    .assign(
        Month=sales_with_cost["Invoice_Date"].dt.to_period("M")
    )
    .groupby("Month")
    .agg(
        Total_Sales=("Total_Sales_Amount", "sum"),
        COGS=("COGS", "sum")
    )
    .reset_index()
)

# Calculate Gross Profit
monthly_gross_profit["Gross_Profit"] = (
    monthly_gross_profit["Total_Sales"]
    - monthly_gross_profit["COGS"]
)

# Monthly Expenses
monthly_expenses = (
    expenses
    .assign(
        Month=expenses["Expense_Date"].dt.to_period("M")
    )
    .groupby("Month")
    .agg(
        Total_Expenses=("Expense_Amount", "sum")
    )
    .reset_index()
)

# Combine Gross Profit and Expenses
monthly_net_profit = monthly_gross_profit.merge(
    monthly_expenses,
    on="Month",
    how="left"
)

# Replace missing expenses with 0
monthly_net_profit["Total_Expenses"] = (
    monthly_net_profit["Total_Expenses"].fillna(0)
)

# Net Profit
monthly_net_profit["Net_Profit"] = (
    monthly_net_profit["Gross_Profit"]
    - monthly_net_profit["Total_Expenses"]
)

# Convert month to readable format
monthly_net_profit["Month_Name"] = (
    monthly_net_profit["Month"]
    .dt.strftime("%b %Y")
)

# Display results
print("\n" + "=" * 75)
print("MONTHLY NET PROFIT ANALYSIS - FY 2025-26")
print("=" * 75)

print(
    monthly_net_profit[
        [
            "Month_Name",
            "Total_Sales",
            "COGS",
            "Gross_Profit",
            "Total_Expenses",
            "Net_Profit"
        ]
    ].to_string(index=False)
)

# ============================================================
# NET PROFIT CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_net_profit["Month_Name"],
    monthly_net_profit["Net_Profit"],
    marker="o"
)

plt.title("Monthly Net Profit Trend - FY 2025-26")
plt.xlabel("Month")
plt.ylabel("Net Profit (₹)")

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================
# STAGE 9 - SALES ANOMALY DETECTION USING IQR
# ============================================================

# Calculate Q1 and Q3
Q1 = sales["Total_Sales_Amount"].quantile(0.25)
Q3 = sales["Total_Sales_Amount"].quantile(0.75)

# Interquartile Range
IQR = Q3 - Q1

# Define upper anomaly threshold
upper_limit = Q3 + (1.5 * IQR)

# Identify unusually high-value sales
sales_anomalies = sales[
    sales["Total_Sales_Amount"] > upper_limit
].copy()

# Sort highest transactions first
sales_anomalies = sales_anomalies.sort_values(
    "Total_Sales_Amount",
    ascending=False
)

print("\n" + "=" * 75)
print("SALES ANOMALY DETECTION - IQR METHOD")
print("=" * 75)

print(f"Q1: ₹{Q1:,.2f}")
print(f"Q3: ₹{Q3:,.2f}")
print(f"IQR: ₹{IQR:,.2f}")
print(f"Upper Anomaly Limit: ₹{upper_limit:,.2f}")

print(f"\nNumber of Unusually High Sales: {len(sales_anomalies)}")

print("\nTop Anomalous Transactions:")

print(
    sales_anomalies[
        [
            "Invoice_ID",
            "Invoice_Date",
            "Customer_ID",
            "Product_ID",
            "Quantity",
            "Total_Sales_Amount"
        ]
    ].head(10).to_string(index=False)
)

# ============================================================
# ANOMALY CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.scatter(
    range(len(sales)),
    sales["Total_Sales_Amount"],
    alpha=0.5
)

plt.axhline(
    upper_limit,
    linestyle="--",
    label=f"Anomaly Threshold ₹{upper_limit:,.0f}"
)

plt.scatter(
    sales.index[sales["Total_Sales_Amount"] > upper_limit],
    sales.loc[
        sales["Total_Sales_Amount"] > upper_limit,
        "Total_Sales_Amount"
    ],
    s=60,
    label="Potential Anomaly"
)

plt.title("Sales Anomaly Detection - IQR Method")
plt.xlabel("Transaction Index")
plt.ylabel("Sales Amount (₹)")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================
# STAGE 10 - SALES FORECASTING
# ============================================================

print("\n" + "=" * 60)
print("SALES FORECAST - NEXT 3 MONTHS")
print("=" * 60)

# Prepare monthly sales
sales["Invoice_Date"] = pd.to_datetime(sales["Invoice_Date"])

monthly_sales_forecast = (
    sales.groupby(
        sales["Invoice_Date"].dt.to_period("M")
    )["Total_Sales_Amount"]
    .sum()
    .reset_index()
)

monthly_sales_forecast.columns = ["Month", "Total_Sales"]

# Convert month to datetime
monthly_sales_forecast["Month"] = (
    monthly_sales_forecast["Month"].dt.to_timestamp()
)

# Sort chronologically
monthly_sales_forecast = monthly_sales_forecast.sort_values("Month")

# Create numeric time index
monthly_sales_forecast["Month_Index"] = range(
    len(monthly_sales_forecast)
)

# Linear trend model
x = monthly_sales_forecast["Month_Index"].values
y = monthly_sales_forecast["Total_Sales"].values

slope, intercept = __import__("numpy").polyfit(x, y, 1)

# Forecast next 3 months
future_index = __import__("numpy").arange(
    len(monthly_sales_forecast),
    len(monthly_sales_forecast) + 3
)

future_sales = slope * future_index + intercept

future_months = pd.date_range(
    start=monthly_sales_forecast["Month"].max()
    + pd.DateOffset(months=1),
    periods=3,
    freq="MS"
)

forecast = pd.DataFrame({
    "Month": future_months,
    "Forecast_Sales": future_sales
})

print("\nHistorical Monthly Sales:")
print(monthly_sales_forecast[["Month", "Total_Sales"]])

print("\nNext 3 Months Sales Forecast:")
print(forecast)

# ============================================================
# FORECAST CHART
# ============================================================

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales_forecast["Month"],
    monthly_sales_forecast["Total_Sales"],
    marker="o",
    label="Actual Sales"
)

plt.plot(
    forecast["Month"],
    forecast["Forecast_Sales"],
    marker="o",
    linestyle="--",
    label="Forecast Sales"
)

plt.title("Monthly Sales Forecast - FY 2025-26")
plt.xlabel("Month")
plt.ylabel("Sales Amount (₹)")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

