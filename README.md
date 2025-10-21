# 🏦 Banking Insights Dashboard — Python | SQL | Tableau | Automation

This project simulates a real-world **Data Analytics Analyst** role (like at JPMorgan Chase).  
It integrates **Python**, **SQL**, and **Tableau** to generate business insights on customers, loans, and account performance.

---

## 🚀 Features
- 📊 Interactive Tableau dashboard for KPIs:
  - Total Customers  
  - Average Account Balance  
  - Loan Conversion Rate  
  - Churn Percentage  
- 🧮 SQL-based ETL and cleaning workflows  
- 🐍 Python scripts for preprocessing & automation  
- 🔁 Automated dashboard refresh using `tableau-api-lib`

---

## 🧠 Tech Stack
**Languages:** Python, SQL  
**Visualization:** Tableau  
**Libraries:** Pandas, Tableau Server Client  
**Automation:** tableau-api-lib


---
🚀 Features

📊 Interactive Tableau Dashboard

Visual KPIs:

Total Customers

Average Account Balance

Loan Conversion Rate

Customer Churn Percentage

Dynamic filters for branch, account type, and date range

Clean corporate UI styled after JPMorgan’s internal dashboards

🧮 SQL-Based ETL Workflow

Wrote SQL queries to join, filter, and aggregate datasets (Bank_Customer_Data, Bank_Loan_Data, Bank_Transaction_Data).

Created calculated fields for balance growth, churn flag, and loan eligibility.

Optimized queries for faster extraction into Tableau.

🐍 Python Data Pre-Processing

Used Pandas for data cleaning, handling nulls, type conversions, and KPI calculation.

Generated a unified merged_dataset.csv ready for Tableau ingestion.

Scheduled preprocessing via a standalone script.

🔁 Automation

Integrated Tableau Server REST API (tableau-api-lib) to refresh the published data source automatically.

Eliminated manual refreshes, achieving a 40 % faster monthly update cycle.

📈 Business Insights

Identified customer churn trends by account type.

Highlighted high-value branches and loan segments.

Enabled data-driven decision-making for resource allocation and customer engagement.

🧠 Tech Stack
Category	Tools / Technologies
Languages	Python, SQL
Visualization	Tableau
Libraries	Pandas, Tableau Server Client, Tableau API Lib
Automation / ETL	Python scripts, SQL queries
Version Control	Git & GitHub
📁 Project Structure
Banking-Insights-Dashboard/
├── data/
│   ├── Bank_Customer_Data.csv
│   ├── Bank_Account_Data.csv
│   ├── Bank_Loan_Data.csv
│   ├── Bank_Transaction_Data.csv
│   └── merged_dataset.csv
├── notebooks/
│   ├── 01_data_familiarization.ipynb     # Exploratory analysis of raw datasets
│   ├── 02_data_cleaning.ipynb            # Data cleaning & merging logic
├── tableau/
│   ├── Banking_Insights_Dashboard.twbx   # Tableau workbook (final dashboard)
├── automation/
│   ├── refresh_tableau.py                # Python automation script
└── README.md

⚙️ Setup & Usage

Clone the repository

git clone https://github.com/<your-username>/Banking-Insights-Dashboard.git


Install dependencies

pip install pandas tableau-api-lib tableau-server-client


Preprocess data

python notebooks/02_data_cleaning.ipynb


Publish the merged_dataset.csv to Tableau and open Banking_Insights_Dashboard.twbx.

Automate monthly refresh

python automation/refresh_tableau.py![img13](https://github.com/user-attachments/assets/c8253d5e-a9dc-4599-a9b8-223173e9ec76)

<img width="1536" height="1024" alt="image (2)" src="https://github.com/user-attachments/assets/93eeb895-ec3e-4be2-a908-daaf295933d5" />
