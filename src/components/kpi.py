from __future__ import annotations

import pandas as pd
import streamlit as st


def _fmt_int(n: int | float | None) -> str:
    if n is None:
        return "—"
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def _fmt_currency(n: float | None) -> str:
    """Format a number as Canadian dollars."""
    if n is None:
        return "—"
    try:
        return f"${n:,.0f}"
    except Exception:
        return str(n)


def show_grant_kpis(df: pd.DataFrame) -> None:
    """Render KPI tiles for grant payments data.

    KPIs:
    - Total grant amount
    - Number of grants
    - Fiscal years covered
    - Number of ministries
    - Number of recipients
    """
    c1, c2, c3, c4 = st.columns(4)

    # Total grant amount
    total_amount = df["Amount"].sum()
    with c1:
        st.metric(label="Total Grants", value=_fmt_currency(total_amount))

    # Number of grants
    total_grants = len(df)
    with c2:
        st.metric(label="Grant Count", value=_fmt_int(total_grants))

    # Fiscal years
    if "DisplayFiscalYear" in df.columns:
        years = df["DisplayFiscalYear"].dropna().unique()
        year_str = f"{len(years)} years"
        with c3:
            st.metric(label="Fiscal Years", value=year_str)
    else:
        with c3:
            st.metric(label="Fiscal Years", value="n/a")

    # Unique recipients
    if "Recipient" in df.columns:
        uniq = df["Recipient"].nunique(dropna=True)
        with c4:
            st.metric(label="Recipients", value=_fmt_int(uniq))
    else:
        with c4:
            st.metric(label="Recipients", value="n/a")
