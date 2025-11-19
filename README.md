
# **Balance Sheet Management (ALM) Gap Analysis Tool**

A Python-based analytical engine designed for **Asset-Liability Management (ALM)** teams to measure **Interest Rate Risk (IRR)** and **Liquidity Risk**.
The tool processes asset and liability cash flows, buckets them into standard time bands, computes **Liquidity** and **Repricing Gaps**, and produces a complete **NII Sensitivity Report** under multiple interest-rate shock scenarios.

---

## 🎯 **Project Overview**

This tool helps financial institutions quantify:

* Liquidity Gap
* Repricing Gap (Rate-Sensitivity Profile)
* Static & Cumulative Gap
* Net Interest Income (NII) sensitivity
* Impact of interest-rate shocks (±100 bps)

---

## ⚡ **Core Functionality**

### **1. Data Ingestion**

* Connects to **PostgreSQL**
* Loads asset & liability cashflow data (300+ rows)

### **2. Bucketing**

Performs:

* **Liquidity Gap bucketing** (based on *maturity_date*)
* **Repricing Gap bucketing** (based on *repricing_date*)

### **3. Gap Calculations**

* **Static Gap** = RSA – RSL in each bucket
* **Cumulative Gap** = Running total across all buckets

### **4. Scenario Analysis**

Simulates **IRR shocks**:

* +100 bps
* –100 bps

Calculates NII changes on the **Rate-Sensitive Position (RSP).**

### **5. Automated Reporting**

Generates:

* Multi-sheet **Excel report**
* Liquidity & Repricing Gap charts (PNG)

---

## 📁 **Project Structure**

```
alm_gap_analysis/
│
├── config.py                       # DB credentials, analysis date, bucket config
├── main.py                         # Entry point (run this file)
├── requirements.txt                # Python dependencies
│
├── data/
│   ├── alm_data.csv                # 300-row dataset
│   └── schema.sql                  # PostgreSQL table definitions
│
├── models/
│   ├── alm_logic.py                # Bucketing + Liquidity & Repricing Gap math
│   └── scenarios.py                # NII sensitivity logic and rate shock analysis
│
└── utils/
    ├── database.py                 # PostgreSQL connection + SQLAlchemy helpers
    └── reporting.py                # Visualization + Excel export
```

---

## ⚙️ **Setup & Execution**

### **1. Prerequisites**

* Python **3.8+**
* PostgreSQL server running locally
* pgAdmin 4 (optional)

---

### **2. Configure Database**

Open **config.py** and update:

```python
DB_CONFIG = {
    'DIALECT': 'postgresql+psycopg2',
    'HOST': 'localhost',
    'DATABASE': 'alm_db',               # <-- create this manually
    'USER': 'postgres',                 # <-- create this manually
    'PASSWORD': 'your_strong_password',
    'PORT': 5432
}
```

### 🔥 **Important**

You **must manually create**:

1. The database:

   ```
   CREATE DATABASE alm_db;
   ```
2. The user:

   ```
   CREATE USER alm_user WITH PASSWORD 'your_strong_password';
   ```
3. Grant privileges:

   ```
   GRANT ALL PRIVILEGES ON DATABASE alm_db TO postgres;
   ```

---

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

### **4. Run the Tool**

```bash
python main.py
```

This will:

* Load data
* Create SQL tables
* Run all ALM analytics
* Generate Excel & chart outputs

---

## 📈 **Output & Interpretation**

After running, the `output/` directory will contain:

### **📘 alm_gap_report.xlsx**

Includes:

#### **Sheet 1 — Liquidity Gap**

* Static Gap (bucket-wise)
* Cumulative Gap
* Liquidity risk indicators
* Funding mismatches

#### **Sheet 2 — Repricing Gap**

* Rate-Sensitive Asset vs. Liability gaps
* IRR exposure profile (asset-sensitive or liability-sensitive)
* Cumulative mismatch (RSP)

#### **Sheet 3 — NII Sensitivity**

Shows ΔNII under shocks:

* +100 bps
* –100 bps

---

### **📊 Charts Generated**

Saved as PNG:

* `liquidity_gap.png`
* `repricing_gap.png`

These visualize static gap distributions across time buckets.

---

## 🧠 **Key ALM Concepts (Used in the Model)**



### Static Gap=RSA−RSL



### Cumulative Gapn ​= i=1∑n​Static Gapi​

### **NII Sensitivity**



### RSP =Rate Sensitive Assets − Rate Sensitive Liabilities

Positive RSP → NII **benefits** from rising rates

Negative RSP → NII **declines** when rates rise

---

## 🧑‍💼 **Who Is This For?**

* Treasury Analysts
* ALM Teams
* Banking Risk Analysts
* Quant Researchers
* Finance Students


