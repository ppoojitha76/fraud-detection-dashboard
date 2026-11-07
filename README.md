
# FinShield Fraud Detection System

## Project Overview

FinShield is a financial fraud detection and data analytics project developed using Python, MySQL, SQL, and Power BI.

The project focuses on analyzing financial transactions, identifying potentially suspicious patterns, and presenting business insights through interactive Power BI dashboards.

The main objective is to understand fraud activity, monitor transaction performance, and identify potential financial risks.

## Project Objectives

- Analyze financial transaction data.
- Identify potentially suspicious transactions.
- Perform SQL-based data analysis.
- Analyze fraud trends and transaction patterns.
- Monitor financial exposure and risk categories.
- Build interactive Power BI dashboards.
- Generate meaningful business insights.

## Technologies Used

| Technology | Purpose |
|---|---|
| MySQL | Database management |
| SQL | Data querying and analysis |
| Power BI | Data visualization |
| Power Query | Data transformation |
| DAX | Measures and KPI calculations |
| Python | Data processing, if used in the project workflow |

## Project Workflow

1. Store and manage transaction data in MySQL.
2. Perform SQL-based data analysis.
3. Analyze potentially suspicious transactions.
4. Identify fraud patterns and risk categories.
5. Connect the database to Power BI.
6. Create interactive dashboards.
7. Analyze business performance and fraud trends.

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

The project SQL file is:

`SQL_queries.sql`

Use MySQL Workbench to review and execute the SQL statements. Check the database and table definitions before running queries.

## Power BI Dashboard

The Power BI report contains two analytical pages.

### Page 1: Executive Dashboard

**Business Objective:** Understand overall transaction performance and fraud activity.

Key Performance Indicators:

- Total Revenue
- Success Rate
- Fraud Cases
- Active Users

Visualizations:

- Revenue Trend
- Fraud Cases by User Location
- Fraud by Payment Method
- High-Risk Fraud Transactions

![Executive Dashboard](executive-dashboard.png)

### Page 2: Fraud Intelligence

**Business Objective:** Investigate fraud patterns, risk distribution, and financial exposure.

Visualizations:

- Risk Category Distribution
- Fraud Cases Trend Over Time
- Fraud Amount by Transaction Type
- Domestic vs International Fraud
- Fraud Rate by Payment Method
- Top 5 Merchants by Fraud Amount

![Fraud Intelligence Dashboard](fraud-intelligence.png)

## Project Execution

### Step 1: Clone the Repository

```bash
git clone https://github.com/ppoojitha76/fraud-detection-dashboard.git
```

### Step 2: Navigate to the Project Folder

```bash
cd fraud-detection-dashboard
```

### Step 3: Configure MySQL

1. Start MySQL Server.
2. Open MySQL Workbench.
3. Create the database if it does not already exist:

```sql
CREATE DATABASE finshield_fraud_detection;
```

4. Open and review `SQL_queries.sql`.
5. Execute the required SQL statements in MySQL Workbench.
6. Configure your local database connection securely.

### Step 4: Open Power BI

1. Open `finshield_dashboard.pbix`.
2. Configure the MySQL connection if required.
3. Refresh the dataset.
4. Explore both dashboard pages.

## Repository Structure

```text
fraud-detection-dashboard/
│
├── README.md
├── SQL_queries.sql
├── finshield_dashboard.pbix
├── executive-dashboard.png
├── fraud-intelligence.png
├── .gitignore
└── LICENSE
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

- Never upload MySQL passwords or database credentials.
- Use secure password prompts or environment variables.
- Do not upload private customer information.
- Use synthetic data for portfolio demonstrations where applicable.
- Review SQL statements before executing them.

## Future Improvements

- Improve fraud detection rules.
- Add data quality validation.
- Analyze repeat suspicious transactions.
- Improve fraud risk analysis.
- Enhance dashboard performance.
- Add automated data processing.

## Author

**CH Poojitha**

Aspiring Data Analyst

**Technical Skills:** SQL | MySQL | Power BI | Python | Excel | DAX

**GitHub:** https://github.com/ppoojitha76

**Project Repository:** https://github.com/ppoojitha76/fraud-detection-dashboard
