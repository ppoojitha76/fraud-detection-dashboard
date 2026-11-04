


# FinShield Fraud Detection System

## Project Overview

FinShield is a financial fraud detection and data analytics project developed using Python, MySQL, SQL, and Power BI.

The project generates synthetic financial transaction records, applies rule-based fraud scoring, stores transaction data in MySQL, and analyzes suspicious transaction patterns through interactive Power BI dashboards.

The main objective is to identify potential fraud patterns, understand financial exposure, and provide useful business insights.

## Project Objectives

- Generate synthetic financial transaction records using Python.
- Apply rule-based fraud detection logic.
- Store transaction records in MySQL.
- Identify potentially suspicious transactions.
- Perform SQL-based data analysis.
- Build interactive Power BI dashboards.
- Analyze fraud trends and transaction risks.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Transaction generation and fraud scoring |
| Jupyter Notebook | Python development |
| Pandas | Data processing |
| MySQL | Database management |
| SQL | Data querying and analysis |
| SQLAlchemy | Database connectivity |
| PyMySQL | MySQL connection |
| Power BI | Data visualization |
| Power Query | Data transformation |
| DAX | Business calculations |

## Project Workflow

1. Generate synthetic transaction records using Python.
2. Connect Python to MySQL.
3. Apply rule-based fraud scoring.
4. Identify transactions flagged for potential fraud.
5. Store transactions and fraud alerts in MySQL.
6. Perform SQL analysis.
7. Connect MySQL to Power BI.
8. Build interactive dashboards.
9. Analyze fraud patterns and business performance.

## Fraud Detection Logic

The project uses rule-based scoring to identify potentially suspicious transactions.

Factors considered include:

- High transaction amounts.
- Customer risk levels.
- International transactions.
- High-risk merchants.
- KYC verification status.
- Unusual transaction activity.

### Risk Categories

| Fraud Score | Risk Category |
|---|---|
| 0–29 | Low Risk |
| 30–59 | Medium Risk |
| 60–100 | High Risk |

These thresholds are project-defined rules. A high-risk score indicates a transaction that may require investigation, not confirmed fraud.

## MySQL Database

**Database Name:** `finshield_fraud_detection`

Main database tables:

- customers
- merchants
- devices
- transactions
- fraud_alerts
- compliance_logs
- live_metrics
- daily_aggregations

## Power BI Dashboard

The Power BI report contains two analytical pages.

### Page 1: Executive Dashboard

**Business Objective:** Understand overall transaction performance and fraud activity.

**Key Performance Indicators:**
- Total Revenue
- Success Rate
- Fraud Cases
- Active Users

**Visualizations:**
- Revenue Trend
- Fraud Cases by User Location
- Fraud by Payment Method
- High-Risk Fraud Transactions

**Business Questions:**
- How is transaction revenue changing?
- Which locations have more fraud cases?
- Which payment methods have higher fraud activity?
- Which transactions require investigation?

### Page 2: Fraud Intelligence

**Business Objective:** Investigate fraud patterns, risk distribution, and financial exposure.

**Visualizations:**
- Risk Category Distribution
- Fraud Cases Trend Over Time
- Fraud Amount by Transaction Type
- Domestic vs International Fraud
- Fraud Rate by Payment Method
- Top 5 Merchants by Fraud Amount

**Business Questions:**
- How are fraud cases changing over time?
- Which transaction types contribute the highest fraud amount?
- Which payment methods have higher fraud rates?
- How do domestic and international fraud cases compare?
- Which merchants have the highest fraud exposure?

## Project Execution

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FinShield-Fraud-Detection
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL

- Install MySQL Server.
- Create the `finshield_fraud_detection` database.
- Execute the database table creation SQL script.
- Configure local database credentials securely.

### 4. Run the Jupyter Notebook

Open:

`Python/finShield_Fraud_Detection.ipynb`

Run the notebook cells in sequence to connect to MySQL and generate transaction records.

Transaction generation is performed manually through Jupyter Notebook. Windows Task Scheduler automation was discontinued because of local laptop performance limitations.

### 5. Open Power BI

- Open the FinShield `.pbix` report.
- Configure the MySQL database connection.
- Refresh the dataset.
- Explore the two dashboard pages.

## Repository Structure

```text
FinShield-Fraud-Detection/
│
├── Python/
│   └── finShield_Fraud_Detection.ipynb
│
├── SQL/
│   ├── create_tables.sql
│   └── sample_queries.sql
│
├── Dashboard/
│   ├── FinShield_Fraud_Detection.pbix
│   └── Screenshots/
│       ├── executive-dashboard.png
│       └── fraud-intelligence.png
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Business Insights

This project helps analyze:

- Overall transaction performance.
- Fraud cases by location.
- Fraud activity by payment method.
- Risk category distribution.
- Fraud amount by transaction type.
- Domestic versus international fraud.
- Fraud rates by payment method.
- Merchants associated with higher fraud amounts.

## Security and Data Handling

- Use synthetic transaction data for portfolio demonstrations.
- Never upload MySQL passwords or database credentials.
- Use secure password prompts or environment variables.
- Do not upload private customer information.
- Clear notebook outputs before publishing.
- Review database cleanup operations before executing the notebook.
- Check the Power BI file for sensitive cached data before publishing.

## Future Improvements

- Improve fraud detection rules.
- Standardize fraud scoring thresholds across Python and Power BI.
- Add data quality validation.
- Analyze repeat suspicious transactions.
- Improve fraud risk analysis.
- Enhance dashboard performance.

## Author

**CH Poojitha**

Data Analytics Portfolio Project

**Technologies:** Python | SQL | MySQL | Power BI | Pandas | DAX
