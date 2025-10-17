from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_grant_payments() -> pd.DataFrame:
    """Load the Alberta grant payments combined CSV.

    Expected schema:
    Ministry, BUName, Recipient, Program, Amount, Lottery,
    PaymentDate, FiscalYear, DisplayFiscalYear
    """
    csv_path = Path(__file__).parent / "grant_disclosure_combined.csv"

    # Read with low_memory=False to avoid dtype warnings on large file
    df = pd.read_csv(csv_path, low_memory=False)

    # Parse PaymentDate
    df["PaymentDate"] = pd.to_datetime(df["PaymentDate"], errors="coerce")

    # Clean Amount: ensure numeric, drop NaNs
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])

    # Clean Ministry: strip whitespace, handle mixed case
    df["Ministry"] = df["Ministry"].astype(str).str.strip().str.upper()

    # DisplayFiscalYear has data quality issues: dates, numbers, and
    # proper fiscal years are mixed. Filter to keep only "YYYY - YYYY" format
    df["DisplayFiscalYear"] = df["DisplayFiscalYear"].astype(str).str.strip()

    # Keep only rows where DisplayFiscalYear matches "YYYY - YYYY" pattern
    # e.g., "2014 - 2015", "2022 - 2023"
    valid_fy_mask = df["DisplayFiscalYear"].str.match(r"^\d{4}\s*-\s*\d{4}$", na=False)
    df = df[valid_fy_mask].copy()

    return df


def load_nonprofits() -> pd.DataFrame:
    """Load the Alberta non-profit organizations data.

    Returns DataFrame with columns:
    Legal Entity Type, Legal Entity Name, Status, Registration Date, City, Postal Code
    """
    xlsx_path = Path(__file__).parent / "non_profit_name_list_for_open_data_portal.xlsx"

    df = pd.read_excel(xlsx_path, skiprows=0)
    df.columns = [
        "Legal Entity Type",
        "Legal Entity Name",
        "Status",
        "Registration Date",
        "City",
        "Postal Code",
    ]
    df = df[1:]  # Skip header row that was in the data

    # Clean up names for better matching
    df["Legal Entity Name"] = (
        df["Legal Entity Name"].astype(str).str.strip().str.upper()
    )

    return df


def load_nonprofits_active() -> pd.DataFrame:
    """Load only active non-profit organizations."""
    df = load_nonprofits()
    return df[df["Status"] == "Active"].copy()


def merge_grants_with_nonprofits(
    grants_df: pd.DataFrame, nonprofits_df: pd.DataFrame
) -> pd.DataFrame:
    """Merge grant data with non-profit data by recipient name.

    Args:
        grants_df: Grant payments DataFrame
        nonprofits_df: Non-profit organizations DataFrame

    Returns:
        Merged DataFrame with grant and non-profit information
    """
    # Prepare grants for merging
    grants = grants_df.copy()
    grants["Recipient_Upper"] = grants["Recipient"].astype(str).str.strip().str.upper()

    # Merge on name
    merged = grants.merge(
        nonprofits_df,
        left_on="Recipient_Upper",
        right_on="Legal Entity Name",
        how="inner",
    )

    return merged


def load_alberta_activity_index() -> pd.DataFrame:
    """Load the Alberta Activity Index time series."""

    xlsx_path = Path(__file__).parent / "alberta-activity-index-data-tables.xlsx"

    df = pd.read_excel(xlsx_path, sheet_name="AAX", skiprows=0)
    if df.empty:
        return pd.DataFrame(columns=["Date", "ActivityIndex"])

    date_col = df.columns[0]
    value_col = df.columns[1]

    df = df.rename(columns={date_col: "Date", value_col: "ActivityIndex"})
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["ActivityIndex"] = pd.to_numeric(df["ActivityIndex"], errors="coerce")
    df = df.dropna(subset=["Date", "ActivityIndex"])

    return df


def load_employment_rates() -> pd.DataFrame:
    """Load Alberta employment rates by sector."""

    csv_path = Path(__file__).parent / "employment_rate.csv"

    df = pd.read_csv(csv_path)
    if df.empty:
        return pd.DataFrame()

    if "year" not in df.columns:
        return pd.DataFrame()

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    value_columns = [c for c in df.columns if c != "year"]
    for col in value_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def load_csv_file(uploaded_file) -> pd.DataFrame:
    """Load a CSV from an uploaded file-like object.

    Attempts to auto-detect grant payment schema or generic columns.
    """
    try:
        df = pd.read_csv(uploaded_file, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="latin-1", low_memory=False)

    # If it looks like grant payments data, normalize
    if "Ministry" in df.columns and "Amount" in df.columns:
        if "PaymentDate" in df.columns:
            df["PaymentDate"] = pd.to_datetime(df["PaymentDate"], errors="coerce")
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Ministry"] = df["Ministry"].astype(str).str.strip().str.upper()
        return df

    # Otherwise, try generic normalization (legacy sample data support)
    for col in ["date", "Date", "DATE"]:
        if col in df.columns:
            df.rename(columns={col: "date"}, inplace=True)
            break
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    rename_map = {}
    for cand in ["Category", "sector", "Sector"]:
        if cand in df.columns and "category" not in df.columns:
            rename_map[cand] = "category"
            break
    for cand in ["Region", "AREA", "Area"]:
        if cand in df.columns and "region" not in df.columns:
            rename_map[cand] = "region"
            break
    for cand in ["Value", "amount", "Amount", "COUNT", "count"]:
        if cand in df.columns and "value" not in df.columns:
            rename_map[cand] = "value"
            break
    if rename_map:
        df.rename(columns=rename_map, inplace=True)

    return df
