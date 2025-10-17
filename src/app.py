import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Local modules
try:  # Support both `streamlit run src/app.py` and `python -m src.app`
    from src.data.loader import (
        load_grant_payments,
        load_nonprofits_active,
        merge_grants_with_nonprofits,
        load_alberta_activity_index,
        load_employment_rates,
    )
    from src.components.kpi import show_grant_kpis
    from src.components.chart import (
        treemap_chart,
        ministry_bar_chart,
        top_programs_by_year_chart,
        programs_by_ministry_chart,
        recipient_totals_chart,
        nonprofit_entity_type_chart,
        nonprofit_top_recipients_chart,
        programs_activity_index_chart,
        employment_rate_grid_chart,
    )
except ModuleNotFoundError:  # Fallback when script dir is `src/`
    from data.loader import (  # type: ignore[import-not-found]
        load_grant_payments,
        load_nonprofits_active,
        merge_grants_with_nonprofits,
        load_alberta_activity_index,
        load_employment_rates,
    )
    from components.kpi import show_grant_kpis  # type: ignore
    from components.chart import (  # type: ignore[import-not-found]
        treemap_chart,
        ministry_bar_chart,
        top_programs_by_year_chart,
        programs_by_ministry_chart,
        recipient_totals_chart,
        nonprofit_entity_type_chart,
        nonprofit_top_recipients_chart,
        programs_activity_index_chart,
        employment_rate_grid_chart,
    )

# Load environment variables
load_dotenv()

APP_TITLE = os.getenv(
    "APP_TITLE",
    "Alberta Grant Distribution Analysis (2014-2024)",
)
PAGE_ICON = os.getenv("PAGE_ICON", "📊")

st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")


@st.cache_data(show_spinner="Loading grant payments...")
def get_grant_payments_cached() -> pd.DataFrame:
    return load_grant_payments()


@st.cache_data(show_spinner="Loading active non-profits...")
def get_nonprofits_active_cached() -> pd.DataFrame:
    return load_nonprofits_active()


@st.cache_data(show_spinner="Loading Alberta Activity Index...")
def get_alberta_activity_index_cached() -> pd.DataFrame:
    return load_alberta_activity_index()


@st.cache_data(show_spinner="Loading employment rates...")
def get_employment_rates_cached() -> pd.DataFrame:
    return load_employment_rates()


df = get_grant_payments_cached()

# --- Main page ---
st.title(APP_TITLE)
st.markdown(
    """
        ### Why This Dashboard Matters

        - **Scale**: 1.2M grant payments worth $330B power Alberta's post-2014
            diversification strategy.
        - **Focus**: Human Services, Health, and Education absorb most dollars,
            signaling sustained social investment.
        - **Trajectory**: Funding nearly doubled from 2014 to 2024.
                        Recipients grew by roughly 25%.

        **Tip:** Use the filters to zero in on ministries, fiscal years, or
        program portfolios.
        """
)

if df.empty:
    st.info("No data loaded. Please check the data source.")
    st.stop()

# --- Filters ---
with st.expander("Filters", expanded=True):
    col1, col2 = st.columns(2)

    # Ministry filter
    if "Ministry" in df.columns:
        ministries = sorted([m for m in df["Ministry"].dropna().unique() if m != ""])
        selected_ministries = col1.multiselect(
            "Ministry",
            options=ministries,
            default=(ministries),
        )
        mask_ministry = (
            df["Ministry"].isin(selected_ministries)
            if selected_ministries
            else pd.Series([True] * len(df))
        )
    else:
        mask_ministry = pd.Series([True] * len(df))

    # Fiscal year filter
    if "DisplayFiscalYear" in df.columns:
        fiscal_years = sorted(
            [fy for fy in df["DisplayFiscalYear"].dropna().unique() if fy != ""]
        )
        selected_fy = col2.multiselect(
            "Fiscal Year", options=fiscal_years, default=fiscal_years
        )
        mask_fy = (
            df["DisplayFiscalYear"].isin(selected_fy)
            if selected_fy
            else pd.Series([True] * len(df))
        )
    else:
        mask_fy = pd.Series([True] * len(df))

    filtered = df[mask_ministry & mask_fy].copy()

if filtered.empty:
    st.warning("No data matches the current filters. Adjust your selection above.")
    st.stop()

# --- KPIs ---
show_grant_kpis(filtered)

st.markdown("---")

# --- Charts ---
# Treemap - Full Width
st.subheader("Grant Distribution (Treemap)")
st.markdown(
    """
    **Quick insight:** Human Services, Health, and Education dominate the
    grant landscape.
    """
)
if {
    "Ministry",
    "Program",
    "Amount",
}.issubset(
    filtered.columns
) and len(filtered) > 0:
    # Treemap: Ministry -> Program
    # Sample for performance if data is large
    treemap_df = filtered
    st.caption(
        "📊 Showing positive grant amounts only. Ministries act as parent"
        " blocks with nested programs."
    )

    fig_treemap = treemap_chart(
        treemap_df,
        path_cols=["Ministry", "Program"],
        value_col="Amount",
        title="Ministry → Program Distribution",
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
    st.markdown(
        """
        **Deeper look:** The treemap confirms how a few ministries anchor
        diversification funding. Within each block you can spot signature
        programs—Human Services channels community safety nets, Health sustains
        preventative care, and Education backs skill development.
        """
    )
else:
    st.info("Treemap requires Ministry, Program, and Amount columns.")

# Total Grants by Ministry - Full Width on Next Row
st.markdown("---")
st.subheader("Total Grants by Ministry")
st.markdown(
    """
    **Quick insight:** Nearly four of every five dollars flow through Human
    Services, Health, and Education.
    """
)
if {"Ministry", "Amount"}.issubset(filtered.columns):
    fig_bar = ministry_bar_chart(
        filtered,
        ministry_col="Ministry",
        value_col="Amount",
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown(
        """
    **Deeper look:** The bar chart shows three ministries towering over the
    rest. That concentration signals deliberate prioritization of social
    infrastructure, while smaller but persistent ministries fund
    agriculture, culture, and innovation niches.
        """
    )
else:
    st.info("Bar chart requires Ministry and Amount columns.")

# --- Top Programs by Year ---
st.markdown("---")
st.subheader("Top Programs by Fiscal Year")
st.markdown(
    """
    **Quick insight:** Year-to-year leaders shift, but social assistance,
    health delivery, and education stay on top.
    """
)
if {
    "DisplayFiscalYear",
    "Program",
    "Ministry",
    "Amount",
}.issubset(filtered.columns):
    fig_year = top_programs_by_year_chart(
        filtered,
        fiscal_year_col="DisplayFiscalYear",
        program_col="Program",
        ministry_col="Ministry",
        value_col="Amount",
        top_n=10,
    )
    st.plotly_chart(fig_year, use_container_width=True)
    st.caption(
        "📊 Shows the top 10 programs each fiscal year and color-codes them"
        " by ministry."
    )
    st.markdown(
        """
        **Deeper look:** Funding pulses in response to economic shocks—the 2016
        and 2020 peaks align with commodity swings and pandemic recovery. The
        mix still leans on education, public safety, and preventative health
        programs.
        """
    )
else:
    st.info(
        "Year chart requires DisplayFiscalYear, Program, Ministry, "
        "and Amount columns."
    )

# --- Block Summary ---
st.markdown("---")
st.markdown(
    """
        #### Distribution Takeaways

        - Nearly 78% of dollars flow through Human Services, Health, and
            Education. That concentration underscores social priorities.
        - Grant value keeps climbing at roughly 5.6% a year despite commodity
            shocks and the pandemic.
        - Unique recipients grow from 2.8K to more than 3.5K. That points to
            wider reach without diluting focus.
        """
)
st.markdown(
    """
    **Deeper look:** Alberta's decade-long grant strategy traces back to
    the 2014 oil price collapse. Rather than doubling down on energy, the
    province redirected dollars into four diversification pillars:

    #### Education & Research
    - Largest growth trajectory across sectors
    - Workforce retraining and skills development
    - Innovation and knowledge infrastructure investments

    #### Healthcare & Social Services
    - Human Services alone channels $4.4B to non-profits—double any other
        ministry
    - Safety nets expand during volatile years
    - Preventative, community-based care takes centre stage

    #### Public Administration
    - Service delivery and governance infrastructure upgrades
    - Digital transformation and efficiency mandates
    - Regulatory and compliance frameworks supported

    #### Agriculture & Rural Development
    - Diversification reaches beyond urban centres
    - Food security and sustainable farming initiatives grow
    - Rural resilience programs reinforce local economies

    **Trendline:** Funding climbs from 830M in 2014-15 to 1.5B in
    2023-24. That is a compound annual growth rate near 5.6%. Recipient
    counts grow by roughly 25%, signalling broader participation without
    losing strategic focus.

    **Anchor recipients:** Legal Aid Society of Alberta (1.08B), Calgary
    Homeless Foundation (252M), Providence Child Development Society
    (200M), Results Driven Agriculture Research (199M), and Renfrew
    Educational Services (194M) act as institutional anchors translating
    policy into province-wide delivery.

    """
)

# --- Programs by Ministry ---
st.markdown("---")
st.subheader("Programs by Ministry")
st.markdown(
    """
        **Quick insight:** Each ministry depends on a short list of signature
        programs to deliver most of its spend.
        """
)
if {"Ministry", "Program", "Amount"}.issubset(filtered.columns):
    tab_top_programs, tab_least_programs = st.tabs(["Top Programs", "Least Programs"])
    with tab_top_programs:
        fig_programs_top = programs_by_ministry_chart(
            filtered,
            ministry_col="Ministry",
            program_col="Program",
            value_col="Amount",
            top_n=5,
            ascending=False,
        )
        st.plotly_chart(fig_programs_top, use_container_width=True)

    with tab_least_programs:
        fig_programs_least = programs_by_ministry_chart(
            filtered,
            ministry_col="Ministry",
            program_col="Program",
            value_col="Amount",
            top_n=5,
            ascending=True,
        )
        st.plotly_chart(fig_programs_least, use_container_width=True)

    st.caption(
        "📊 Highlights the highest and lowest funded programs within each" " ministry."
    )
else:
    st.info("Program charts require Ministry, Program, and Amount columns.")

# --- Recipient Totals ---
st.markdown("---")
st.subheader("Recipient Totals")
st.markdown(
    """
    **Quick insight:** A small cohort of anchor organizations absorbs the
    largest cheques, while hundreds of micro-recipients split modest grants.
    """
)
if {"Recipient", "Amount"}.issubset(filtered.columns):
    tab_top_recipients, tab_least_recipients = st.tabs(
        ["Top Recipients", "Least Recipients"]
    )
    with tab_top_recipients:
        fig_recipients_top = recipient_totals_chart(
            filtered,
            recipient_col="Recipient",
            value_col="Amount",
            top_n=15,
            ascending=False,
        )
        st.plotly_chart(fig_recipients_top, use_container_width=True)

    with tab_least_recipients:
        fig_recipients_least = recipient_totals_chart(
            filtered,
            recipient_col="Recipient",
            value_col="Amount",
            top_n=15,
            ascending=True,
        )
        st.plotly_chart(fig_recipients_least, use_container_width=True)

    st.caption(
        "📊 Compares recipients by the total dollars received across "
        "the filtered dataset."
    )
    st.markdown(
        """
        **Deeper look:** Large social service agencies provide province-wide
        coverage, while the long tail captures hyper-local projects. Watch how
        the mix shifts when you filter by ministry or year to validate reach.
        """
    )
else:
    st.info("Recipient charts require Recipient and Amount columns.")

# --- Recipient Summary ---
st.markdown("---")
st.markdown(
    """
        #### Recipient Takeaways

        - Anchor recipients handle province-wide mandates, while the long tail
            keeps niche and local pilots funded.
        - Apply ministry or year filters to confirm whether dollars stay with
            incumbents or rotate toward emerging partners.
        """
)

# --- Non-Profit Analysis ---
st.markdown("---")
st.header("Non-Profit Organizations: The Implementation Layer")
st.markdown(
    """
        **Why it matters:** Join 1.2M grant payments with 27,634 active
        non-profits to see who turns policy into services.
        """
)
st.markdown(
    """
        - 214,394 payments align with active entities inside the provincial
            registry.
        - $8.8B flows through 6,391 organizations, roughly 8% of the filtered
            spend.
        - Human Services, Health, and Education channel 78% of these dollars.
        - Alberta Societies account for 74% of recipients, anchoring community
            reach.
        """
)
st.markdown(
    """
    **Deeper look:** Three ministries dominate non-profit flows—Human
    Services ($4.4B), Health ($2.2B), and Education ($2.2B). Alberta
    Societies handle grassroots delivery, non-profit companies contribute
    professional services, extra-provincial corps fill national gaps, and
    agricultural societies bolster rural resilience. Together they validate a
    diversified delivery model that mirrors the province's policy thesis.
    """
)

try:
    # Load active non-profits and merge with filtered grants
    with st.spinner("Loading non-profit data..."):
        nonprofits_active = get_nonprofits_active_cached()
        nonprofit_grants = merge_grants_with_nonprofits(
            filtered,
            nonprofits_active,
        )

    if len(nonprofit_grants) > 0:
        # KPIs for non-profits
        col1, col2, col3 = st.columns(3)
        with col1:
            total_np_amount = nonprofit_grants["Amount"].sum()
            st.metric(
                "Total to Active Non-Profits",
                f"${total_np_amount:,.0f}",
            )
        with col2:
            unique_np = nonprofit_grants["Legal Entity Name"].nunique()
            st.metric("Unique Active Non-Profits", f"{unique_np:,}")
        with col3:
            percent_of_total = (total_np_amount / filtered["Amount"].sum()) * 100
            st.metric(
                "% of Total Grants",
                f"{percent_of_total:.1f}%",
            )

        st.caption(
            "Snapshot of the active non-profit channel within the current"
            " filter selection."
        )
        st.markdown("---")

        # Bar chart of top non-profits by total grant amount
        st.subheader("Top Active Non-Profit Recipients by Grant Amount")
        st.markdown(
            """
            **Quick insight:** Province-wide anchors such as Legal Aid and the
            Calgary Homeless Foundation lead the funding table.
            """
        )
        fig_np_top = nonprofit_top_recipients_chart(
            nonprofit_grants,
            recipient_col="Legal Entity Name",
            value_col="Amount",
            entity_type_col="Legal Entity Type",
            top_n=25,
        )
        st.plotly_chart(fig_np_top, use_container_width=True)
        st.caption(
            "📊 Active non-profit organizations ranked by total grant amount"
            " and color-coded by entity type."
        )
        st.markdown(
            """
            **Deeper look:** These organizations operate at provincial scale,
            delivering justice access, homelessness programs, and specialized
            education. Their funding stability confirms the government's
            reliance on institutional anchors for critical services.
            """
        )

        st.markdown("---")

        # Entity type summary
        st.subheader("Grants by Entity Type")
        st.markdown(
            """
            **Quick insight:** Alberta Societies dominate, yet non-profit
            companies still capture meaningful funding.
            """
        )
        fig_np_entity = nonprofit_entity_type_chart(
            nonprofit_grants,
            entity_type_col="Legal Entity Type",
            value_col="Amount",
            top_n=15,
        )
        st.plotly_chart(fig_np_entity, use_container_width=True)
        st.caption("📊 Total grant dollars by non-profit organization type.")
        st.markdown(
            """
            **Deeper look:** Societies cover grassroots delivery, companies add
            specialized expertise, and extra-provincial groups plug national
            gaps—together signalling a diversified delivery chain.
            """
        )

        st.markdown("---")
        st.subheader("Actual Economic Value")
        try:
            activity_index_df = get_alberta_activity_index_cached()
            st.markdown(
                """
                **Quick insight:** Grant momentum moves in tandem with the
                Alberta Activity Index, especially during recovery years.
                """
            )
            fig_grant_vs_index = programs_activity_index_chart(
                filtered,
                fiscal_year_col="DisplayFiscalYear",
                program_col="Program",
                value_col="Amount",
                top_n=10,
                activity_index_df=activity_index_df,
            )
            st.plotly_chart(fig_grant_vs_index, use_container_width=True)
            st.caption(
                "📊 Compares top program totals against the Alberta Activity"
                " Index to show momentum versus macro trends."
            )
            st.markdown(
                """
                **Deeper look:** The curves lift together when policy makers
                lean into expansions and ease during slowdowns. Matching peaks
                in 2016 and 2020 show grants reinforcing economic cycles rather
                than smoothing them.
                """
            )
        except Exception as activity_err:
            st.warning(
                "Could not load the Alberta Activity Index dataset: " f"{activity_err}"
            )

        st.markdown("---")
        st.subheader("Employment Rate Trends by Sector")
        try:
            employment_df = get_employment_rates_cached()
            st.markdown(
                """
                **Quick insight:** Health, education, agriculture, and public
                services hold their employment gains through the decade.
                """
            )
            fig_employment = employment_rate_grid_chart(employment_df)
            st.plotly_chart(fig_employment, use_container_width=True)
            st.caption(
                "📈 Sector employment rates (2014-2025) with a dashed 2020"
                " marker to highlight the pandemic inflection point."
            )
            st.markdown(
                """
                **Deeper look:** The sectors receiving sustained grants are the
                only ones with steady post-2014 job growth. Energy-adjacent
                industries sag, confirming grants are reinforcing resilient
                sectors rather than chasing laggards.
                    """
            )
        except Exception as employment_err:
            st.warning(
                "Could not load the employment rate dataset: " f"{employment_err}"
            )

    else:
        st.info(
            "No grants matched with active non-profit organizations in the "
            "current filter selection."
        )

except Exception as e:
    st.error(f"Error loading non-profit data: {e}")
    st.info(
        "Non-profit analysis requires the non_profit_name_list_for_open_data_"
        "portal.xlsx file in the data directory."
    )


st.markdown("---")
st.subheader("Conclusion")
st.markdown(
    """
    Alberta's fiscal policy now synthetically props up social ministries by
    recycling ever-larger grant pools. The visuals show that despite a decade
    of rising allocations, employment in these grant-dependent fields merely
    treads water while self-sustaining industries stagnate or shrink. That
    dynamic traps the province in a feedback loop—Public Administration,
    Education, Health, and Human Services keep the jobs supplied by grants,
    yet the underlying problems linger and deepen.

    Increasing award amounts keep the current workforce afloat, but they no
    longer expand opportunity. If other sectors continue to erode, the tax
    base that funds these grants will thin, forcing difficult trade-offs even
    as signature campaigns such as the green dividend succeed (a story beyond
    this dashboard). The charts imply that future decisions must confront this
    structural imbalance: redirect capital toward genuinely productive fields,
    demand measurable sustainability from social programs, or accept a tighter
    fiscal horizon where grant-driven employment is the ceiling rather than a
    bridge to broader growth.
        """
)
st.markdown("---")
st.caption("Data source: Alberta Government Grant Payments Disclosure. ")

st.markdown(
    """
    #### Contact / CTA
    - **Portfolio Showcase**: This app was built with Streamlit to
      demonstrate skills in data analysis and interactive visualization.
    - **Email**: borisenko1315@gmail.com
    """
)
