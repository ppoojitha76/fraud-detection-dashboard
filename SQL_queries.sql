CREATE DATABASE  finshield_fraud_detection;
-- 1. Select your database
USE finshield_fraud_detection;



-- 2. Create Customers Table
CREATE TABLE Customers (
    Customer_ID VARCHAR(20) PRIMARY KEY,
    Full_Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    City VARCHAR(50),
    State VARCHAR(50),
    Pincode VARCHAR(10),
    Account_Type VARCHAR(20),
    Account_Created_Date DATE,
    Risk_Score INT DEFAULT 50,
    Is_Active BOOLEAN DEFAULT TRUE,
    Customer_Segment VARCHAR(20),
    KYC_Verified BOOLEAN DEFAULT FALSE,
    Last_Transaction_Date DATETIME,
    Total_Transactions_Lifetime INT DEFAULT 0,
    Total_Amount_Lifetime DECIMAL(15,2) DEFAULT 0
);
-- 3. Create Merchants Table
CREATE TABLE Merchants (
    Merchant_ID VARCHAR(20) PRIMARY KEY,
    Merchant_Name VARCHAR(100),
    Category VARCHAR(50),
    Sub_Category VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    Pincode VARCHAR(10),
    Registration_Date DATE,
    Is_Verified BOOLEAN DEFAULT FALSE,
    Risk_Level VARCHAR(20) DEFAULT 'Low',
    Annual_Revenue_Estimate DECIMAL(15,2),
    Settlement_Days INT DEFAULT 2
);

-- 4. Create Devices Table
CREATE TABLE Devices (
    Device_ID VARCHAR(20) PRIMARY KEY,
    Device_Type VARCHAR(20),
    OS VARCHAR(20),
    Browser VARCHAR(20),
    Is_Trusted_Device BOOLEAN DEFAULT FALSE,
    Device_Fingerprint VARCHAR(100)
);

-- 5. Create Transactions Table (Main Fact Table)
CREATE TABLE Transactions (
    Transaction_ID VARCHAR(50) PRIMARY KEY,
    Customer_ID VARCHAR(20),
    Merchant_ID VARCHAR(20),
    Device_ID VARCHAR(20),
    Amount DECIMAL(12,2),
    Payment_Method VARCHAR(20),
    Transaction_Type VARCHAR(20),
    Transaction_Status VARCHAR(20),
    Fraud_Score INT DEFAULT 0,
    Is_Fraud BOOLEAN DEFAULT FALSE,
    Is_International BOOLEAN DEFAULT FALSE,
    Latitude DECIMAL(10,8),
    Longitude DECIMAL(11,8),
    User_Location VARCHAR(100),
    IP_Address VARCHAR(20),
    Transaction_Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Settlement_Date DATE,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Merchant_ID) REFERENCES Merchants(Merchant_ID),
    FOREIGN KEY (Device_ID) REFERENCES Devices(Device_ID)
);

-- 6. Create Fraud Alerts Table
CREATE TABLE Fraud_Alerts (
    Alert_ID INT AUTO_INCREMENT PRIMARY KEY,
    Transaction_ID VARCHAR(50),
    Alert_Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Fraud_Score INT,
    Risk_Category VARCHAR(50),
    Reason VARCHAR(200),
    Action_Taken VARCHAR(50) DEFAULT 'Under Review',
    Assigned_To VARCHAR(50),
    Resolution_Date DATETIME
);

-- 7. Create Live Metrics Table (Updated Every Minute)
CREATE TABLE Live_Metrics (
    Metric_ID INT AUTO_INCREMENT PRIMARY KEY,
    Metric_Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Total_Transactions_1min INT,
    Total_Amount_1min DECIMAL(15,2),
    Success_Rate_Percent DECIMAL(5,2),
    Fraud_Count_1min INT,
    Avg_Transaction_Amount DECIMAL(10,2),
    Avg_Response_Time_ms INT,
    Top_Merchant VARCHAR(100),
    High_Risk_Transactions_Count INT,
    Unique_Customers_1min INT,
    Unique_Merchants_1min INT,
    UPI_Usage_Percent DECIMAL(5,2),
    International_Transactions INT
);

-- 8. Create Daily Aggregations Table
CREATE TABLE Daily_Aggregations (
    Date DATE PRIMARY KEY,
    Total_Transactions INT,
    Total_Revenue DECIMAL(15,2),
    Success_Rate DECIMAL(5,2),
    Fraud_Count INT,
    Fraud_Amount DECIMAL(15,2),
    Avg_Transaction_Value DECIMAL(10,2),
    Unique_Customers INT,
    Unique_Merchants INT,
    Top_Region VARCHAR(50),
    Top_Category VARCHAR(50),
    Churn_Rate DECIMAL(5,2),
    Revenue_Growth_Percent DECIMAL(5,2)
);

-- 9. Create Compliance Logs Table
CREATE TABLE Compliance_Logs (
    Log_ID INT AUTO_INCREMENT PRIMARY KEY,
    Log_Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Report_Type VARCHAR(50),
    Transaction_ID VARCHAR(50),
    Threshold_Exceeded DECIMAL(15,2),
    Reporting_Status VARCHAR(20) DEFAULT 'Pending',
    Submitted_To VARCHAR(50)
);

-- 10. Verify all tables are created
SHOW TABLES;

-- Check transactions growing
SELECT COUNT(*) FROM transactions;
-- Check fraud alerts
SELECT COUNT(*) FROM fraud_alerts;

-- Check live metrics
SELECT * FROM live_metrics ORDER BY Metric_Timestamp DESC LIMIT 5;

-- See recent transactions
SELECT Transaction_ID, Amount, Payment_Method, Transaction_Status, Fraud_Score 
FROM transactions 
ORDER BY Transaction_Timestamp DESC 
LIMIT 10;


-- 6. Fraud by payment method
SELECT Payment_Method, 
       COUNT(*) AS Fraud_Count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions WHERE Is_Fraud = TRUE), 2) AS Percentage
FROM transactions
WHERE Is_Fraud = TRUE
GROUP BY Payment_Method
ORDER BY Fraud_Count DESC;
SELECT COUNT(*) AS Total_Rows
FROM Transactions;
-- 7. Daily revenue trend (last 7 days)
SELECT DATE(Transaction_Timestamp) AS Date, 
       SUM(Amount) AS Daily_Revenue,
       COUNT(*) AS Transaction_Count
FROM transactions
WHERE Transaction_Status = 'Success'
GROUP BY DATE(Transaction_Timestamp)
ORDER BY Date DESC
LIMIT 7;

-- 8. Top 10 merchants by revenue
SELECT m.Merchant_Name, 
       COUNT(t.Transaction_ID) AS Transaction_Count,
       SUM(t.Amount) AS Total_Revenue
FROM transactions t
JOIN merchants m ON t.Merchant_ID = m.Merchant_ID
WHERE t.Transaction_Status = 'Success'
GROUP BY m.Merchant_Name
ORDER BY Total_Revenue DESC
LIMIT 10;

-- 9. Customers with most transactions
SELECT c.Full_Name, 
       COUNT(t.Transaction_ID) AS Transaction_Count,
       SUM(t.Amount) AS Total_Spent
FROM transactions t
JOIN customers c ON t.Customer_ID = c.Customer_ID
GROUP BY c.Full_Name
ORDER BY Transaction_Count DESC
LIMIT 10;

-- 10. Success rate by payment method
SELECT Payment_Method,
       COUNT(*) AS Total_Transactions,
       SUM(CASE WHEN Transaction_Status = 'Success' THEN 1 ELSE 0 END) AS Success_Count,
       ROUND(SUM(CASE WHEN Transaction_Status = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Success_Rate
FROM transactions
GROUP BY Payment_Method
ORDER BY Success_Rate DESC;
SELECT SUM(Amount) AS Total_Revenue
FROM transactions;
SHOW TABLES;


SELECT
    COUNT(*) AS Total_Rows,
    SUM(Amount) AS Total_Revenue,
    MAX(Amount) AS Max_Amount,
    MIN(Amount) AS Min_Amount
FROM transactions;

SELECT COUNT(*) AS Total_Rows
FROM transactions;

Select version(),current_user();