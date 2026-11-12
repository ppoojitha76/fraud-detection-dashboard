#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine, text  # ← THIS IS THE IMPORTANT LINE!
import pymysql
from faker import Faker
import random
from datetime import datetime, timedelta
import time

print("✅ Libraries imported!")



# In[2]:


# ==========================================
# YOUR MYSQL CREDENTIALS
# ==========================================

username = "root"
password = "Poojithamysql098"  

# Correct format: NO extra @ symbol
DATABASE_URL = f"mysql+pymysql://{username}:{password}@localhost:3306/finshield_fraud_detection"

print("🔧 Connection URL created (password hidden)")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ Connected to MySQL successfully!")
    print(f"📊 Database: finshield_fraud_detection")

    # Check tables
    tables = pd.read_sql("SHOW TABLES", engine)
    print(f"✅ Found {len(tables)} tables:")
    for table in tables.iloc[:, 0]:
        print(f"   - {table}")

except Exception as e:
    print(f"❌ Connection failed: {e}")


# In[5]:


# ==========================================
# CELL 4: Transaction Generator with Fraud Scoring
# ==========================================

def generate_transaction():

    """Generate a single transaction with fraud scoring"""

    # Load reference data
    customers_df = pd.read_sql("SELECT Customer_ID, Risk_Score, City, KYC_Verified, Customer_Segment FROM customers", engine)
    merchants_df = pd.read_sql("SELECT Merchant_ID, Risk_Level FROM merchants", engine)
    devices_df = pd.read_sql("SELECT Device_ID FROM devices", engine)

    # Select random entities
    customer = customers_df.sample(1).iloc[0]
    merchant = merchants_df.sample(1).iloc[0]
    device = devices_df.sample(1).iloc[0]

    # Amount based on customer segment
    segment_amounts = {
        'Retail': (10, 5000),
        'HNI': (100, 100000),
        'SME': (500, 25000),
        'Corporate': (1000, 500000)
    }
    min_amt, max_amt = segment_amounts.get(customer['Customer_Segment'], (10, 10000))
    amount = round(random.uniform(min_amt, max_amt), 2)

    # Payment method
    payment_method = random.choices(
        ['UPI', 'Credit Card', 'Debit Card', 'Net Banking'],
        weights=[0.55, 0.15, 0.2, 0.1]
    )[0]

    if payment_method == 'UPI':
        amount = min(amount, 10000)

    # International?
    is_international = random.choices([True, False], weights=[0.05, 0.95])[0]

    # --- FRAUD SCORING ENGINE ---
    fraud_score = 0
    reasons = []
    risk_category = None

    # Rule 1: High amount + Low risk customer
    if amount > 25000 and customer['Risk_Score'] < 30:
        fraud_score += 35
        reasons.append("High amount with low risk customer")
        risk_category = 'High Amount'

    # Rule 2: High risk customer
    if customer['Risk_Score'] > 80:
        fraud_score += 30
        reasons.append("High risk customer")
        risk_category = 'High Risk Customer'

    # Rule 3: International from domestic location
    if is_international and customer['City'] in ['Mumbai', 'Delhi', 'Bangalore']:
        fraud_score += 25
        reasons.append("International from domestic location")
        risk_category = 'Suspicious Location'

    # Rule 4: High risk merchant
    if merchant['Risk_Level'] == 'High':
        fraud_score += 20
        reasons.append("High risk merchant")

    # Rule 5: KYC not verified
    if not customer['KYC_Verified'] and amount > 10000:
        fraud_score += 25
        reasons.append("KYC not verified")

    # Rule 6: Unusual hours (12 AM - 5 AM)
    current_hour = datetime.now().hour
    if 0 <= current_hour <= 5:
        fraud_score += 15
        reasons.append("Unusual hours")
        risk_category = 'Unusual Pattern'

    # Rule 7: Random fraud (5% chance)
    if random.random() < 0.05:
        fraud_score += random.randint(30, 50)
        reasons.append("Random fraud flag")

    # Cap at 100
    fraud_score = min(fraud_score, 100)

    # Determine status
    status = 'Success'
    is_fraud = False

    if fraud_score > 60:
        is_fraud = True
        status = 'Flagged'
    elif random.random() < 0.06:
        status = 'Failed'
    elif random.random() < 0.02:
        status = 'Pending'

    # Location
    lat = round(random.uniform(8.0, 37.0), 6)
    lon = round(random.uniform(68.0, 97.0), 6)

    transaction = {
        'Transaction_ID': f'TXN{datetime.now().strftime("%Y%m%d%H%M%S")}{random.randint(100,999)}',
        'Customer_ID': customer['Customer_ID'],
        'Merchant_ID': merchant['Merchant_ID'],
        'Device_ID': device['Device_ID'],
        'Amount': amount,
        'Payment_Method': payment_method,
        'Transaction_Type': random.choices(['Payment', 'Refund'], weights=[0.95, 0.05])[0],
        'Transaction_Status': status,
        'Fraud_Score': fraud_score,
        'Is_Fraud': is_fraud,
        'Is_International': is_international,
        'Latitude': lat,
        'Longitude': lon,
        'User_Location': customer['City'],
        'IP_Address': fake.ipv4(),
        'Transaction_Timestamp': datetime.now(),
        'Settlement_Date': datetime.now() + timedelta(days=2)
    }

    # --- Log Fraud Alerts ---
    if is_fraud:
        alert = {
            'Transaction_ID': transaction['Transaction_ID'],
            'Alert_Timestamp': datetime.now(),
            'Fraud_Score': fraud_score,
            'Risk_Category': risk_category or 'Multiple Rules',
            'Reason': ' | '.join(reasons),
            'Action_Taken': 'Under Review',
            'Assigned_To': None,
            'Resolution_Date': None
        }
        pd.DataFrame([alert]).to_sql('fraud_alerts', engine, if_exists='append', index=False)
        print(f"🚨 FRAUD! {transaction['Transaction_ID']} - Score: {fraud_score}")

    # --- Compliance: Large Transaction ---
    if amount > 500000:
        compliance = {
            'Log_Timestamp': datetime.now(),
            'Report_Type': 'Large Transaction Report',
            'Transaction_ID': transaction['Transaction_ID'],
            'Threshold_Exceeded': amount,
            'Reporting_Status': 'Pending',
            'Submitted_To': None
        }
        pd.DataFrame([compliance]).to_sql('compliance_logs', engine, if_exists='append', index=False)

    return transaction

print("✅ Transaction generator ready!")


# In[6]:


# ==========================================
# CELL 5: Update Live Metrics (FIXED)
# ==========================================

from sqlalchemy import text  # ← IMPORTANT!

def update_live_metrics():
    """Calculate 1-minute aggregations"""
    query = """
    INSERT INTO live_metrics (
        Metric_Timestamp, Total_Transactions_1min, Total_Amount_1min, 
        Success_Rate_Percent, Fraud_Count_1min, Avg_Transaction_Amount, 
        Avg_Response_Time_ms, High_Risk_Transactions_Count,
        Unique_Customers_1min, Unique_Merchants_1min, UPI_Usage_Percent,
        International_Transactions
    )
    SELECT 
        NOW(),
        COUNT(*),
        SUM(Amount),
        ROUND(SUM(CASE WHEN Transaction_Status = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2),
        SUM(CASE WHEN Is_Fraud = TRUE THEN 1 ELSE 0 END),
        ROUND(AVG(Amount), 2),
        ROUND(AVG(CASE WHEN Transaction_Status = 'Success' THEN 30 + (Amount/1000) * 5 ELSE 0 END), 0),
        SUM(CASE WHEN Fraud_Score > 50 THEN 1 ELSE 0 END),
        COUNT(DISTINCT Customer_ID),
        COUNT(DISTINCT Merchant_ID),
        ROUND(SUM(CASE WHEN Payment_Method = 'UPI' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2),
        SUM(CASE WHEN Is_International = TRUE THEN 1 ELSE 0 END)
    FROM transactions
    WHERE Transaction_Timestamp >= NOW() - INTERVAL 1 MINUTE
    """
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()
    print(f"📈 Live metrics updated at {datetime.now().strftime('%H:%M:%S')}")

print("✅ Live metrics function ready!")


# In[7]:


# ==========================================
# CELL 6: Update Daily Aggregations (FIXED)
# ==========================================

def update_daily_aggregations():
    """Calculate daily summary"""
    query = """
    INSERT INTO daily_aggregations (Date, Total_Transactions, Total_Revenue, 
                                    Success_Rate, Fraud_Count, Fraud_Amount,
                                    Avg_Transaction_Value, Unique_Customers, 
                                    Unique_Merchants, Top_Region, Top_Category)
    SELECT 
        CURDATE(),
        COUNT(*),
        SUM(Amount),
        ROUND(SUM(CASE WHEN Transaction_Status = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2),
        SUM(CASE WHEN Is_Fraud = TRUE THEN 1 ELSE 0 END),
        SUM(CASE WHEN Is_Fraud = TRUE THEN Amount ELSE 0 END),
        ROUND(AVG(Amount), 2),
        COUNT(DISTINCT Customer_ID),
        COUNT(DISTINCT Merchant_ID),
        (SELECT City FROM customers WHERE Customer_ID = transactions.Customer_ID LIMIT 1),
        (SELECT Category FROM merchants WHERE Merchant_ID = transactions.Merchant_ID LIMIT 1)
    FROM transactions
    WHERE DATE(Transaction_Timestamp) = CURDATE()
    """
    with engine.connect() as conn:
        conn.execute(text(query))  # ← ADD "text()" HERE!
        conn.commit()
    print(f"📊 Daily aggregation updated for {datetime.now().strftime('%Y-%m-%d')}")

print("✅ Daily aggregation function ready!")


# In[7]:


# ==========================================
# CELL 7: Delete Old Data (FIXED)
# ==========================================

from sqlalchemy import text  # ← ADD THIS IMPORT!

def delete_old_data():
    """Delete transactions older than 7 days"""
    query = """
    DELETE FROM transactions 
    WHERE Transaction_Timestamp < NOW() - INTERVAL 7 DAY
    """
    with engine.connect() as conn:
        conn.execute(text(query))  # ← ADD "text()" HERE!
        conn.commit()

    query2 = """
    DELETE FROM fraud_alerts 
    WHERE Alert_Timestamp < NOW() - INTERVAL 7 DAY
    """
    with engine.connect() as conn:
        conn.execute(text(query2))  # ← ADD "text()" HERE!
        conn.commit()

    query3 = """
    DELETE FROM live_metrics 
    WHERE Metric_Timestamp < NOW() - INTERVAL 1 DAY
    """
    with engine.connect() as conn:
        conn.execute(text(query3))  # ← ADD "text()" HERE!
        conn.commit()

    print("🗑️ Old data deleted (kept last 7 days)")

print("✅ Delete function ready!")


# In[8]:


from faker import Faker

fake = Faker()

print("Faker imported successfully")


# In[9]:


print(fake.name())


# In[ ]:


# ==========================================
# CELL 8: RUN THE STREAMING PIPELINE
# ==========================================

print("\n🚀 Starting FinShield Fraud Detection Pipeline...")
print("⏰ Streaming every 2 seconds...")
print("📊 Pipeline will run for 10 minutes.\n")

transaction_count = 0
last_daily_update = datetime.now().date()
last_cleanup = datetime.now().date()

try:
    for _ in range(300):

        # Generate and insert transaction
        txn = generate_transaction()
        pd.DataFrame([txn]).to_sql(
            'transactions',
            engine,
            if_exists='append',
            index=False
        )

        transaction_count += 1

        # Update live metrics every 30 transactions
        if transaction_count % 30 == 0:
            update_live_metrics()

        # Daily aggregation
        current_date = datetime.now().date()

        if current_date != last_daily_update:
            update_daily_aggregations()
            last_daily_update = current_date

        # Delete old data daily
        if current_date != last_cleanup:
            delete_old_data()
            last_cleanup = current_date

        # Progress indicator every 10 transactions
        if transaction_count % 10 == 0:
            status_emoji = (
                "✅" if txn['Transaction_Status'] == 'Success'
                else "⚠️" if txn['Transaction_Status'] == 'Failed'
                else "🚨"
            )

            print(
                f"{status_emoji} TXN {transaction_count}: "
                f"₹{txn['Amount']} | "
                f"{txn['Payment_Method']} | "
                f"{txn['Transaction_Status']}"
            )

        time.sleep(2)

    print(f"\n✅ Pipeline completed. Total transactions: {transaction_count}")

except KeyboardInterrupt:
    print(f"\n🛑 Stopped. Total transactions: {transaction_count}")

except Exception as e:
    print(f"❌ Error: {e}")


# In[ ]:


import pandas as pd
from sqlalchemy import create_engine, text  # ← THIS IS THE IMPORTANT LINE!
import pymysql
from faker import Faker
import random
from datetime import datetime, timedelta
import time

print("✅ Libraries imported!")



# In[ ]:





# In[ ]:


txn = generate_transaction()
pd.DataFrame([txn]).to_sql('transactions', engine, if_exists='append', index=False)
transaction_count += 1
print(txn)

