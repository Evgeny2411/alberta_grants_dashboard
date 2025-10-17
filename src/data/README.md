# Data Preprocessing

This directory contains the grant payments disclosure data and preprocessing scripts.

## Files

### Combined Data

- **`grant_disclosure_combined.csv`** - Combined dataset from all source files (1.8M+ rows)
  - Years covered: 2014-2024
  - Unique ministries: 69
  - Total grant amount: $435+ billion

### Source Files

- `Grant Payments Disclosure YYYY-YY.csv` - Annual grant payment reports
- `TBF Grants Disclosure YYYY-YY.csv` - Treasury Board Finance grant reports

### Scripts

- **`preprocess_and_combine.py`** - Main preprocessing script
- **`loader.py`** - Data loading utilities for the Streamlit app

## Data Schema

The combined dataset has the following columns:

| Column            | Type     | Description                                 |
| ----------------- | -------- | ------------------------------------------- |
| Ministry          | string   | Government ministry name                    |
| BUName            | string   | Business unit name                          |
| Recipient         | string   | Grant recipient name                        |
| Program           | string   | Program name                                |
| Amount            | float    | Grant amount in CAD                         |
| Lottery           | boolean  | Whether funded by lottery proceeds          |
| PaymentDate       | datetime | Date of payment                             |
| FiscalYear        | integer  | Fiscal year (e.g., 2014, 2015)              |
| DisplayFiscalYear | string   | Formatted fiscal year (e.g., "2014 - 2015") |

## Preprocessing

The preprocessing script handles several data quality issues:

### Issues Resolved

1. **Encoding Problems**

   - Files use different encodings (UTF-8, Latin-1, CP1252)
   - Script tries multiple encodings automatically

2. **Commas in Quoted Fields**

   - Some ministry names contain commas (e.g., "ARTS, CULTURE AND STATUS OF WOMEN")
   - CSV parser properly handles quoted fields

3. **Inconsistent Column Structures**

   - All files standardized to common schema
   - Missing columns filled with NaN

4. **Data Cleaning**
   - Extra whitespace removed
   - Quote characters stripped
   - Empty strings converted to NaN

### Running the Preprocessing

To regenerate the combined file:

```bash
# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Run preprocessing script
python src/data/preprocess_and_combine.py
```

Output:

```
======================================================================
Grant Payments Disclosure - Preprocessing and Combining
======================================================================

Found 12 grant disclosure files to process:
  - Grant Payments Disclosure 2014-15.csv
  - Grant Payments Disclosure 2015-16.csv
  ...
  ✅ Successfully saved 1,835,224 rows to grant_disclosure_combined.csv
```

## Data Quality Notes

### Known Issues

1. Some rows have negative amounts (corrections/reversals)
2. DisplayFiscalYear format varies slightly between files
3. Ministry names may have changed over time
4. Some recipient names contain special characters

### Validation

- All files validated for required columns
- Amount field converted to numeric (invalid values become NaN)
- Dates parsed and validated
- Boolean fields standardized

## Usage in App

The `loader.py` module provides functions to load data:

```python
from src.data.loader import load_grant_payments

# Load combined dataset
df = load_grant_payments()

# Upload custom CSV
from src.data.loader import load_csv_file
df = load_csv_file(uploaded_file)
```

## Data Sources

All data sourced from:

- Alberta Government Open Data Portal
- Treasury Board and Finance Grant Disclosure Reports
- Public accountability and transparency initiatives
