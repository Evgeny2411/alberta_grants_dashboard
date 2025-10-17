from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Professional color palettes
MINISTRY_COLORS = px.colors.qualitative.Set3
PROGRAM_COLORS = px.colors.qualitative.Pastel
ENTITY_COLORS = px.colors.qualitative.Bold
SEQUENTIAL_COLORS = px.colors.sequential.Teal
DIVERGING_COLORS = px.colors.diverging.RdYlBu


def treemap_chart(
    df: pd.DataFrame,
    *,
    path_cols: list[str],
    value_col: str,
    title: str = "Grant Distribution",
) -> go.Figure:
    """Create a treemap chart showing hierarchical grant distribution.

    Args:
        df: DataFrame with grant data
        path_cols: Hierarchical path columns (e.g., ['Ministry', 'Program'])
        value_col: Column with numeric values to aggregate
        title: Chart title
    """
    # Aggregate by path
    agg = df.groupby(path_cols, dropna=False, as_index=False)[value_col].sum()

    # Treemap requires positive values - filter out negatives and zeros
    agg = agg[agg[value_col] > 0].copy()

    if len(agg) == 0:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No positive amounts to display",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    agg = agg.sort_values(value_col, ascending=False)  # type: ignore

    # Limit to top values to avoid overcrowding
    # Keep top 500 program entries
    if len(agg) > 500:
        agg = agg.head(500)

    fig = px.treemap(
        agg,
        path=path_cols,
        values=value_col,
        title=title,
        height=600,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_traces(
        textposition="middle center",
        hovertemplate=(
            "<b>%{label}</b><br>Amount: $%{value:,.0f}<br>"
            "%{percentParent}<extra></extra>"
        ),
        marker=dict(line=dict(color="white", width=2), cornerradius=5),
    )
    fig.update_layout(
        margin=dict(l=8, r=8, t=40, b=8),
        font=dict(size=12),
        title_font=dict(size=18, color="#2c3e50"),
    )
    return fig


def ministry_bar_chart(
    df: pd.DataFrame, *, ministry_col: str, value_col: str
) -> go.Figure:
    """Create a horizontal bar chart of total grants by ministry.

    Args:
        df: DataFrame with grant data
        ministry_col: Column with ministry names
        value_col: Column with numeric values to aggregate
    """
    agg = df.groupby(ministry_col, dropna=True, as_index=False)[value_col].sum()
    agg = agg.sort_values(value_col, ascending=True)  # type: ignore

    fig = px.bar(
        agg,
        x=value_col,
        y=ministry_col,
        orientation="h",
        title="Total Grants by Ministry (All Years)",
        labels={value_col: "Total Amount ($)", ministry_col: "Ministry"},
        color=value_col,
        color_continuous_scale="Teal",
    )
    fig.update_layout(
        margin=dict(l=8, r=8, t=40, b=8),
        yaxis=dict(automargin=True),
        font=dict(size=12),
        title_font=dict(size=18, color="#2c3e50"),
        showlegend=False,
    )
    fig.update_traces(
        marker=dict(line=dict(color="rgba(255,255,255,0.6)", width=1)),
    )
    return fig


def top_programs_by_year_chart(
    df: pd.DataFrame,
    *,
    fiscal_year_col: str,
    program_col: str,
    ministry_col: str,
    value_col: str,
    top_n: int = 10,
) -> go.Figure:
    """Create a stacked bar chart of top programs by fiscal year.

    Shows the top N programs each year, color-coded by ministry.

    Args:
        df: DataFrame with grant data
        fiscal_year_col: Column with fiscal year strings
        program_col: Column with program names
        ministry_col: Column with ministry names
        value_col: Column with numeric values to aggregate
        top_n: Number of top programs to show per year
    """
    # Extract start year from fiscal year string (e.g., "2014 - 2015" -> 2014)
    df_copy = df.copy()
    df_copy["Year"] = df_copy[fiscal_year_col].str.extract(r"^(\d{4})")[0].astype(int)

    # Aggregate by year, ministry, program
    agg = (
        df_copy.groupby(["Year", ministry_col, program_col], dropna=False)[value_col]
        .sum()
        .reset_index()
    )

    # Get top N programs per year
    top_programs_per_year = []
    for year in sorted(agg["Year"].unique()):
        year_data = agg[agg["Year"] == year].copy()
        year_data = year_data.nlargest(top_n, value_col)
        top_programs_per_year.append(year_data)

    plot_df = pd.concat(top_programs_per_year, ignore_index=True)

    # Create stacked bar chart
    fig = px.bar(
        plot_df,
        x="Year",
        y=value_col,
        color=ministry_col,
        hover_data=[program_col],
        title=f"Top {top_n} Programs by Year (Color: Ministry)",
        labels={value_col: "Amount ($)", "Year": "Fiscal Year (Start)"},
        height=500,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )

    fig.update_layout(
        xaxis=dict(tickmode="linear", dtick=1),
        yaxis=dict(title="Total Amount ($)"),
        legend=dict(title="Ministry", orientation="v", x=1.02, y=1),
        margin=dict(l=50, r=150, t=50, b=50),
        hovermode="closest",
        font=dict(size=12),
        title_font=dict(size=18, color="#2c3e50"),
        plot_bgcolor="rgba(245,245,245,0.5)",
    )

    # Format hover template
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Year: %{x}<br>"
            "Amount: $%{y:,.0f}<br>"
            "Ministry: %{fullData.name}<extra></extra>"
        ),
        marker=dict(line=dict(color="white", width=0.5)),
    )

    return fig


def programs_activity_index_chart(
    df: pd.DataFrame,
    *,
    fiscal_year_col: str,
    program_col: str,
    value_col: str,
    top_n: int,
    activity_index_df: pd.DataFrame,
) -> go.Figure:
    """Combine top program grants with the Alberta Activity Index."""

    def _empty(msg: str) -> go.Figure:
        fig = go.Figure()
        fig.add_annotation(
            text=msg,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    required_cols = {fiscal_year_col, program_col, value_col}
    if not required_cols.issubset(df.columns):
        return _empty("Missing columns for grant vs index comparison")

    if activity_index_df.empty:
        return _empty("Alberta Activity Index data not available")

    df_copy = df[list(required_cols)].copy()
    df_copy[value_col] = pd.to_numeric(df_copy[value_col], errors="coerce")
    df_copy = df_copy[df_copy[value_col].notna()]
    df_copy = df_copy[df_copy[value_col] > 0]

    df_copy["Year"] = df_copy[fiscal_year_col].astype(str).str.extract(r"^(\d{4})")[0]
    df_copy = df_copy.dropna(subset=["Year"])

    if df_copy.empty:
        return _empty("No grant values available for comparison")

    df_copy["Year"] = df_copy["Year"].astype(int)

    grouped = (
        df_copy.groupby(["Year", program_col], dropna=False)[value_col]
        .sum()
        .reset_index()
    )

    if grouped.empty:
        return _empty("Not enough program data to calculate trends")

    top_n = max(1, top_n)
    top_per_year = (
        grouped.sort_values(value_col, ascending=False)
        .groupby("Year", group_keys=False)
        .head(top_n)
    )

    totals = (
        top_per_year.groupby("Year")[value_col]
        .sum()
        .reset_index()
        .rename(columns={value_col: "GrantAmount"})
    )

    if totals.empty:
        return _empty("Top program totals could not be calculated")

    if not {"Date", "ActivityIndex"}.issubset(activity_index_df.columns):
        return _empty("Alberta Activity Index columns missing")

    aai = activity_index_df.copy()
    aai["Date"] = pd.to_datetime(aai["Date"], errors="coerce")
    aai["ActivityIndex"] = pd.to_numeric(
        aai["ActivityIndex"],
        errors="coerce",
    )
    aai = aai.dropna(subset=["Date", "ActivityIndex"])

    if aai.empty:
        return _empty("Alberta Activity Index data not available")

    aai["Year"] = aai["Date"].dt.year
    aai_yearly = aai.groupby("Year")["ActivityIndex"].mean().reset_index()

    combined = totals.merge(aai_yearly, on="Year", how="left")
    combined = combined.sort_values("Year")

    if combined.empty:
        return _empty("No overlapping grant and index data to plot")

    grant_billions = combined["GrantAmount"] / 1_000_000_000

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(
        x=combined["Year"],
        y=grant_billions,
        name="Top Program Grants",
        customdata=combined["GrantAmount"],
        hovertemplate=(
            "Year %{x}<br>Grant Total: $%{customdata:,.0f}"
            "<br>Billions: %{y:.2f}<extra></extra>"
        ),
        marker=dict(
            color=grant_billions,
            colorscale="Tealgrn",
            line=dict(color="white", width=1),
        ),
    )

    fig.add_scatter(
        x=combined["Year"],
        y=combined["ActivityIndex"],
        name="Alberta Activity Index",
        mode="lines+markers",
        line=dict(width=4, color="#e67e22"),
        marker=dict(size=9, color="#e67e22", symbol="diamond"),
        hovertemplate="Year %{x}<br>Index: %{y:.2f}<extra></extra>",
        secondary_y=True,
    )

    fig.update_yaxes(
        title_text="Top Program Grants ($ billions)",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Alberta Activity Index (avg)",
        secondary_y=True,
    )
    fig.update_xaxes(title_text="Fiscal Year (start)")
    fig.update_layout(
        title="Grant Momentum vs Alberta Activity Index",
        margin=dict(l=50, r=40, t=60, b=40),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            xanchor="left",
        ),
        font=dict(size=12),
        title_font=dict(size=18, color="#2c3e50"),
        plot_bgcolor="rgba(245,245,245,0.5)",
    )

    return fig


def employment_rate_grid_chart(
    df: pd.DataFrame,
    *,
    year_col: str = "year",
    rows: int = 5,
    cols: int = 3,
) -> go.Figure:
    """Render a grid of employment rate time series charts."""

    if df.empty or year_col not in df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Employment rate data unavailable",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    sectors = [col for col in df.columns if col != year_col]
    if not sectors:
        fig = go.Figure()
        fig.add_annotation(
            text="No sector columns found in employment data",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    total_slots = rows * cols
    titles: list[str] = []
    for idx in range(total_slots):
        if idx < len(sectors):
            titles.append(sectors[idx].replace("_", " ").title())
        else:
            titles.append("")

    subplot = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=False,
        subplot_titles=titles,
        vertical_spacing=0.06,
        horizontal_spacing=0.08,
    )

    years = df[year_col].astype(int)
    tick_vals = years.tolist()
    tick_text = [str(year) for year in tick_vals]
    y_max = df[sectors].max().max()
    y_limit = 0.0 if pd.isna(y_max) else float(y_max) * 1.1
    y_limit = max(1.0, y_limit)

    for idx, sector in enumerate(sectors):
        row = idx // cols + 1
        col = idx % cols + 1
        values = df[sector]

        # Use a color from a palette based on sector index
        color_palette = px.colors.qualitative.Set2
        line_color = color_palette[idx % len(color_palette)]

        subplot.add_trace(
            go.Scatter(
                x=years,
                y=values,
                mode="lines+markers",
                name=sector.replace("_", " ").title(),
                line=dict(width=3, color=line_color),
                marker=dict(size=6, color=line_color),
                hovertemplate=(
                    "Year %{x}<br>Employment Index: %{y:.1f}<extra></extra>"
                ),
                showlegend=False,
            ),
            row=row,
            col=col,
        )

        subplot.add_vline(  # type: ignore[arg-type]
            x=2020,
            line_dash="dash",
            line_color="#e74c3c",
            line_width=2,
            row=row,
            col=col,
        )

        subplot.update_xaxes(
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_text,
            showticklabels=True,
            showgrid=False,
            row=row,
            col=col,
        )
        subplot.update_yaxes(
            range=[0, y_limit],
            showgrid=True,
            gridcolor="#dddddd",
            row=row,
            col=col,
        )

    for empty_idx in range(len(sectors), total_slots):
        row = empty_idx // cols + 1
        col = empty_idx % cols + 1
        subplot.update_xaxes(visible=False, row=row, col=col)
        subplot.update_yaxes(visible=False, row=row, col=col)

    for col_idx in range(1, cols + 1):
        subplot.update_xaxes(title_text="Year", row=rows, col=col_idx)
    for row_idx in range(1, rows + 1):
        subplot.update_yaxes(title_text="Employment Index", row=row_idx, col=1)

    subplot.update_layout(
        title="Employment Rates by Sector",
        height=1500,
        margin=dict(l=60, r=40, t=70, b=60),
        hovermode="closest",
        font=dict(size=11),
        title_font=dict(size=20, color="#2c3e50"),
        plot_bgcolor="rgba(250,250,250,0.8)",
        paper_bgcolor="white",
    )

    return subplot


def programs_by_ministry_chart(
    df: pd.DataFrame,
    *,
    ministry_col: str,
    program_col: str,
    value_col: str,
    top_n: int = 5,
    ascending: bool = False,
    max_ministries: int | None = 6,
    title: str | None = None,
) -> go.Figure:
    """Create a faceted bar chart of programs grouped by ministry."""

    if top_n <= 0:
        top_n = 1

    agg = df.groupby([ministry_col, program_col], dropna=False, as_index=False)[
        value_col
    ].sum()
    agg[value_col] = pd.to_numeric(agg[value_col], errors="coerce")
    agg = agg[agg[value_col].notna()]
    agg = agg[agg[value_col] > 0]

    if agg.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No positive grant amounts available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    agg[ministry_col] = agg[ministry_col].fillna("Unknown Ministry")
    agg[program_col] = agg[program_col].fillna("Unknown Program")

    ministry_totals = (
        agg.groupby(ministry_col)[value_col].sum().sort_values(ascending=False)
    )
    if max_ministries is not None and max_ministries > 0:
        selected_ministries = ministry_totals.head(max_ministries).index
        agg = agg[agg[ministry_col].isin(selected_ministries)].copy()

    agg_sorted = agg.sort_values(
        by=[value_col], ascending=ascending
    )  # type: ignore[arg-type]
    plot_df = agg_sorted.groupby(ministry_col, group_keys=False).head(top_n).copy()

    if plot_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Not enough program data to display",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    plot_df["_rank"] = plot_df.groupby(ministry_col)[value_col].rank(
        method="first", ascending=ascending
    )
    plot_df = plot_df.sort_values(
        by=[ministry_col, "_rank"], ascending=[True, ascending]
    )

    chart_title = (
        title
        if title
        else (f"{'Least' if ascending else 'Top'} {top_n} Programs per Ministry")
    )

    fig = px.bar(
        plot_df,
        x=value_col,
        y=program_col,
        facet_col=ministry_col,
        facet_col_wrap=3,
        orientation="h",
        title=chart_title,
        labels={
            value_col: "Total Amount ($)",
            program_col: "Program",
            ministry_col: "Ministry",
        },
        color=value_col,
        color_continuous_scale="Viridis",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Ministry: %{facet_col}<br>"
            "Amount: $%{x:,.0f}<extra></extra>"
        ),
        marker=dict(line=dict(color="rgba(255,255,255,0.6)", width=1)),
    )
    fig.update_yaxes(matches=None, automargin=True)
    fig.update_yaxes(
        categoryorder="total descending" if ascending else "total ascending"
    )
    fig.update_layout(
        margin=dict(l=50, r=50, t=60, b=30),
        font=dict(size=11),
        title_font=dict(size=18, color="#2c3e50"),
        showlegend=False,
    )

    return fig


def recipient_totals_chart(
    df: pd.DataFrame,
    *,
    recipient_col: str,
    value_col: str,
    top_n: int = 15,
    ascending: bool = False,
    title: str | None = None,
) -> go.Figure:
    """Create a bar chart of recipients ordered by total grant amount."""

    if top_n <= 0:
        top_n = 1

    agg = df.groupby(recipient_col, dropna=True, as_index=False)[value_col].sum()
    agg[value_col] = pd.to_numeric(agg[value_col], errors="coerce")
    agg = agg[agg[value_col].notna()]
    agg = agg[agg[value_col] > 0]

    if agg.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No recipient totals available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    agg[recipient_col] = agg[recipient_col].fillna("Unknown Recipient")

    if ascending:
        selected = agg.sort_values(by=[value_col], ascending=True).head(
            top_n
        )  # type: ignore[arg-type]
    else:
        selected = agg.sort_values(by=[value_col], ascending=False).head(
            top_n
        )  # type: ignore[arg-type]

    if selected.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Not enough recipient data to display",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    display_df = selected.sort_values(value_col, ascending=True).copy()

    chart_title = (
        title
        if title
        else (f"{'Least' if ascending else 'Top'} {len(display_df)} Recipients")
    )

    fig = px.bar(
        display_df,
        x=value_col,
        y=recipient_col,
        orientation="h",
        title=chart_title,
        labels={
            value_col: "Total Amount ($)",
            recipient_col: "Recipient",
        },
        color=value_col,
        color_continuous_scale="Bluered",
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Amount: $%{x:,.0f}<extra></extra>",
        marker=dict(line=dict(color="rgba(255,255,255,0.6)", width=1)),
    )
    fig.update_yaxes(
        categoryorder="total descending" if ascending else "total ascending",
        automargin=True,
    )
    fig.update_layout(
        margin=dict(l=60, r=40, t=60, b=30),
        font=dict(size=12),
        title_font=dict(size=18, color="#2c3e50"),
        showlegend=False,
    )

    return fig


def time_series_chart(
    df: pd.DataFrame,
    *,
    date_col: str,
    value_col: str,
    color_col: str | None = None,
):
    """Legacy time series chart for generic data."""
    plot_df = df.dropna(subset=[date_col, value_col]).copy()
    if color_col and color_col in plot_df.columns:
        fig = px.line(
            plot_df,
            x=date_col,
            y=value_col,
            color=color_col,
            markers=True,
        )
    else:
        fig = px.line(
            plot_df,
            x=date_col,
            y=value_col,
            markers=True,
        )
    fig.update_layout(margin=dict(l=16, r=16, t=32, b=16))
    return fig


def bar_chart(df: pd.DataFrame, *, category_col: str, value_col: str):
    """Legacy bar chart for generic data."""
    agg = df.groupby(category_col, dropna=True, as_index=False)[value_col].sum()
    fig = px.bar(agg, x=category_col, y=value_col)
    fig.update_layout(margin=dict(l=16, r=16, t=32, b=16))
    return fig


def nonprofit_entity_type_chart(
    df: pd.DataFrame,
    *,
    entity_type_col: str,
    value_col: str,
    top_n: int = 15,
) -> go.Figure:
    """Create a bar chart of grant totals by non-profit entity type."""
    agg = df.groupby(entity_type_col, dropna=False, as_index=False)[value_col].sum()
    agg[value_col] = pd.to_numeric(agg[value_col], errors="coerce")
    agg = agg[agg[value_col].notna()]
    agg = agg[agg[value_col] > 0]

    if agg.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No entity type data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    agg = agg.sort_values(value_col, ascending=True)  # type: ignore

    if len(agg) > top_n:
        agg = agg.tail(top_n)

    fig = px.bar(
        agg,
        x=value_col,
        y=entity_type_col,
        orientation="h",
        title=f"Top {len(agg)} Non-Profit Entity Types by Grant Amount",
        labels={
            value_col: "Total Grant Amount ($)",
            entity_type_col: "Entity Type",
        },
        color=value_col,
        color_continuous_scale="Sunset",
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Total: $%{x:,.0f}<extra></extra>",
        marker=dict(line=dict(color="rgba(255,255,255,0.6)", width=1)),
    )
    fig.update_layout(
        margin=dict(l=50, r=40, t=60, b=30),
        yaxis=dict(automargin=True),
        font=dict(size=12),
        title_font=dict(size=18, color="#2c3e50"),
        showlegend=False,
    )
    return fig


def nonprofit_top_recipients_chart(
    df: pd.DataFrame,
    *,
    recipient_col: str,
    value_col: str,
    entity_type_col: str,
    top_n: int = 20,
) -> go.Figure:
    """Create a bar chart of top non-profit recipients with entity type info."""
    agg = df.groupby([recipient_col, entity_type_col], dropna=False)[value_col].sum()
    agg = agg.reset_index()
    agg[value_col] = pd.to_numeric(agg[value_col], errors="coerce")
    agg = agg[agg[value_col].notna()]
    agg = agg[agg[value_col] > 0]

    if agg.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No non-profit recipient data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    agg = agg.sort_values(value_col, ascending=False).head(top_n)  # type: ignore
    agg = agg.sort_values(value_col, ascending=True)  # type: ignore

    fig = px.bar(
        agg,
        x=value_col,
        y=recipient_col,
        color=entity_type_col,
        orientation="h",
        title=f"Top {len(agg)} Active Non-Profit Grant Recipients",
        labels={
            value_col: "Total Grant Amount ($)",
            recipient_col: "Non-Profit Organization",
            entity_type_col: "Entity Type",
        },
        height=max(400, len(agg) * 25),
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Type: %{fullData.name}<br>"
            "Total: $%{x:,.0f}<extra></extra>"
        ),
        marker=dict(line=dict(color="white", width=0.5)),
    )
    fig.update_layout(
        margin=dict(l=50, r=40, t=60, b=30),
        yaxis=dict(automargin=True),
        legend=dict(title="Entity Type"),
        font=dict(size=12),
        title_font=dict(size=18, color="#2c3e50"),
    )
    return fig


def nonprofit_grant_distribution_treemap(
    df: pd.DataFrame,
    *,
    entity_type_col: str,
    recipient_col: str,
    value_col: str,
    max_items: int = 100,
) -> go.Figure:
    """Create a treemap of non-profit grants by entity type and recipient."""
    agg = df.groupby([entity_type_col, recipient_col], dropna=False)[value_col].sum()
    agg = agg.reset_index()
    agg[value_col] = pd.to_numeric(agg[value_col], errors="coerce")
    agg = agg[agg[value_col].notna()]
    agg = agg[agg[value_col] > 0]

    if agg.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No non-profit grant data to display",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    agg = agg.sort_values(value_col, ascending=False)  # type: ignore

    if len(agg) > max_items:
        agg = agg.head(max_items)

    fig = px.treemap(
        agg,
        path=[entity_type_col, recipient_col],
        values=value_col,
        title="Non-Profit Grant Distribution by Entity Type",
        height=600,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(
        textposition="middle center",
        hovertemplate=(
            "<b>%{label}</b><br>Amount: $%{value:,.0f}<br>"
            "%{percentParent}<extra></extra>"
        ),
        marker=dict(line=dict(color="white", width=2), cornerradius=5),
    )
    fig.update_layout(
        margin=dict(l=8, r=8, t=40, b=8),
        font=dict(size=12),
        title_font=dict(size=18, color="#2c3e50"),
    )
    return fig
