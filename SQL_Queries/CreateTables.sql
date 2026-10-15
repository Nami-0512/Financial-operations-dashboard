USE Financial_Operations_DB;
GO

-- 1. Customers
CREATE TABLE Customers (
    Customer_ID VARCHAR(20) NOT NULL,
    Customer_Name VARCHAR(100) NOT NULL,
    City VARCHAR(50),
    Customer_Type VARCHAR(50),
    Contact_Number VARCHAR(20),
    Credit_Limit DECIMAL(18,2),
    CONSTRAINT PK_Customers PRIMARY KEY (Customer_ID)
);
GO

-- 2. Products
CREATE TABLE Products (
    Product_ID VARCHAR(20) NOT NULL,
    Brand VARCHAR(50) NOT NULL,
    Product_Model VARCHAR(100),
    Category VARCHAR(50),
    Cost_Price DECIMAL(18,2) NOT NULL,
    Selling_Price DECIMAL(18,2) NOT NULL,
    CONSTRAINT PK_Products PRIMARY KEY (Product_ID)
);
GO

-- 3. Sales Invoices
CREATE TABLE Sales_Invoices (
    Invoice_ID VARCHAR(20) NOT NULL,
    Invoice_Date DATE NOT NULL,
    Customer_ID VARCHAR(20) NOT NULL,
    Product_ID VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL,
    Unit_Selling_Price DECIMAL(18,2) NOT NULL,
    Total_Sales_Amount DECIMAL(18,2) NOT NULL,
    Due_Date DATE NOT NULL,
    Payment_Status VARCHAR(20),
    CONSTRAINT PK_Sales_Invoices PRIMARY KEY (Invoice_ID),
    CONSTRAINT FK_Sales_Customer
        FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    CONSTRAINT FK_Sales_Product
        FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID)
);
GO

-- 4. Purchases
CREATE TABLE Purchases (
    Purchase_ID VARCHAR(20) NOT NULL,
    Purchase_Date DATE NOT NULL,
    Supplier_Name VARCHAR(100),
    Product_ID VARCHAR(20) NOT NULL,
    Quantity_Purchased INT NOT NULL,
    Unit_Cost DECIMAL(18,2) NOT NULL,
    Total_Purchase_Amount DECIMAL(18,2) NOT NULL,
    CONSTRAINT PK_Purchases PRIMARY KEY (Purchase_ID),
    CONSTRAINT FK_Purchases_Product
        FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID)
);
GO

-- 5. Payments
CREATE TABLE Payments (
    Payment_ID VARCHAR(20) NOT NULL,
    Invoice_ID VARCHAR(20) NOT NULL,
    Customer_ID VARCHAR(20) NOT NULL,
    Payment_Date DATE NOT NULL,
    Amount_Paid DECIMAL(18,2) NOT NULL,
    Payment_Mode VARCHAR(30),
    CONSTRAINT PK_Payments PRIMARY KEY (Payment_ID),
    CONSTRAINT FK_Payments_Invoice
        FOREIGN KEY (Invoice_ID) REFERENCES Sales_Invoices(Invoice_ID),
    CONSTRAINT FK_Payments_Customer
        FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)
);
GO

-- 6. Expenses
CREATE TABLE Expenses (
    Expense_ID VARCHAR(20) NOT NULL,
    Expense_Date DATE NOT NULL,
    Expense_Category VARCHAR(50) NOT NULL,
    Expense_Amount DECIMAL(18,2) NOT NULL,
    Remarks VARCHAR(255),
    CONSTRAINT PK_Expenses PRIMARY KEY (Expense_ID)
);
GO