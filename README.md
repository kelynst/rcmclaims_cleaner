# 🏥 rcmclaims_cleaner  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


A lightweight Python tool for **cleaning and validating healthcare claims data**.  
It demonstrates how to use **Pandas** for real-world data preprocessing — useful for RCM (Revenue Cycle Management), healthcare analytics, or insurance data projects.  

---

## 📌 Project Overview  
- **Goal** → Provide a simple script to clean raw claims data (remove blanks, normalize dates, drop duplicates).  
- **Approach** → Load `.csv` / `.xlsx` files with Pandas, apply cleaning rules, save clean outputs.  
- **Status** → Beginner-friendly portfolio project, extendable to real healthcare pipelines.  

---

## 📂 Repo Structure  
rcmclaims_cleaner/
│── claims_cleaner.py     # Main script
│── requirements.txt      # Dependencies
│── sample_claims.xlsx    # Example dataset (fake claims)
│── README.md             # Project documentation
│── .gitignore            # Ignore virtual envs, caches, CSVs

---

## ✅ Features  
- Handles **CSV or Excel input**.  
- Cleans data by:  
  - Removing empty rows/columns.  
  - Normalizing **dates** into consistent ISO format.  
  - Dropping duplicates.  
- Saves output as `cleaned_<filename>.csv`.  
- Beginner-friendly but extendable for real RCM workflows.  

---

## 📦 Requirements  
- Python 3.10+  
- `pip` (Python package manager)  
- Dependencies listed in `requirements.txt`  

To install requirements manually:  
```bash
pip install -r requirements.txt
```

---

## 🚀 Installation  

1. 📥 Clone the repository  
```bash
git clone https://github.com/kelynst/rcmclaims_cleaner.git
cd rcmclaims_cleaner
```
2. 🌱 Create a virtual environment  
```bash
python3 -m venv .venv
```
3. ⚡ Activate the virtual environment  
**macOS/Linux**
```bash
source .venv/bin/activate
```
**Windows (Powershell)**
```bash
 .venv\Scripts\Activate
 ```
4. 📦 Install dependencies  
```bash
pip install -r requirements.txt
```
---

## ▶️ Usage  

**Clean an example file**  
 ```bash 
python claims_cleaner.py sample_claims.csv
 ```
**Clean a custom CSV**  
```bash 
python claims_cleaner.py my_claims.csv
```
- A new file is created in the same folder named:  cleaned_sample_claims.csv

---

## 📝 Example Run  

**Input (sample_claims.csv)**  
| PatientID | DOB       | DOS       | Amount | Notes       |  
|-----------|-----------|-----------|--------|-------------|  
| 101       | 01/02/1980| 2025-01-05| 200    | follow-up   |  
| 101       | 01/02/1980| 2025-01-05| 200    | follow-up   |  
| 102       |           | 2025-02-15| 500    |             |  

**Run command**  
```bash
python clean_claims.py sample_claims.csv
```


```
✅ Clean complete  
• Input:  sample_claims.csv  
• Output: cleaned_sample_claims.csv  
• Rows: 3 → 3 (after empty-row drop) → 2 (after dedup)  
• Cols: 5 → 5  
• Date columns normalized: DOB, DOS  
```



---

## 🔮 Future Improvements  
- Validate patient IDs against external reference list.  
- Add billing code normalization (ICD-10/CPT).  
- Integrate HL7/FHIR input support.  
- Export cleaned results directly to database.  

---

## 🤝 Contributing  
Fork the repo and submit PRs with improvements. Ideas: add rules, integrate APIs, build dashboards.  

---

## ⚠️ Notes  
- Example dataset is **fake** (not real patient data).  
- Always use HIPAA-compliant data handling for real healthcare projects.  
- CSVs, `.venv`, and caches are ignored via `.gitignore`.  

---

## 📜 License  
MIT License — see LICENSE.  