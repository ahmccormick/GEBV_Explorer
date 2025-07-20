import streamlit as st
import pandas as pd
import altair as alt

# 1) App title
st.title("🧬 Welcome to GEBV Explorer")

# 2) Load and merge data
qpath = "/Users/annamccormick/R/World_Veg_Project/data/outputs/GEBV_quality_core_16traits_n423.csv"
apath = "/Users/annamccormick/R/World_Veg_Project/data/outputs/GEBVs_core_13_agronomic_traits_avg.csv"

df_q = pd.read_csv(qpath)
df_a = pd.read_csv(apath)

if "Group" in df_a.columns and "Group" in df_q.columns:
    df = pd.merge(df_q, df_a, on=["Line", "Group"], how="inner")
else:
    df = pd.merge(df_q, df_a, on="Line", how="inner")

# 3) Sidebar sliders (initialize full range)
trait_cols = [c for c in df.columns if c.startswith("GEBV_")]
st.sidebar.header("Thresholds")
thresholds = {}
for col in trait_cols:
    lo, hi = float(df[col].min()), float(df[col].max())
    thresholds[col] = st.sidebar.slider(
        label=col,
        min_value=lo,
        max_value=hi,
        value=(lo, hi),       # full range by default
        help=f"Select {col} between {lo:.2f} and {hi:.2f}"
    )

# 4) Apply filter
mask = pd.Series(True, index=df.index)
for col, (lo, hi) in thresholds.items():
    mask &= df[col].between(lo, hi)
filtered = df[mask]

# 5) Display filtered table
st.write(f"Lines passing all thresholds: **{len(filtered)}**")
st.dataframe(filtered)

# 6) All-lines expander
with st.expander("Show all lines (unfiltered)"):
    st.dataframe(df)

# 7) Scatter plot layering with fixed defaults
st.write("---")
st.subheader("Scatter plot of two traits")

# Determine default positions for yield and Brix
default_x = trait_cols.index("GEBV_Brix") if "GEBV_Brix" in trait_cols else 0
default_y = trait_cols.index("GEBV_yield")  if "GEBV_yield"  in trait_cols else 1

col1, col2 = st.columns(2)
with col1:
    x_sel = st.selectbox(
        "X-axis trait",
        trait_cols,
        index=default_x
    )
with col2:
    y_sel = st.selectbox(
        "Y-axis trait",
        trait_cols,
        index=default_y
    )

if x_sel and y_sel:
    # Base layer: all points in gray
    base = (
        alt.Chart(df)
        .mark_circle(size=60, color="lightgray")
        .encode(
            x=alt.X(x_sel,  type="quantitative"),
            y=alt.Y(y_sel,  type="quantitative"),
            tooltip=["Line", x_sel, y_sel],
        )
    )
    # Highlight layer: filtered points in red
    highlight = (
        alt.Chart(filtered)
        .mark_circle(size=60, color="red")
        .encode(
            x=alt.X(x_sel, type="quantitative"),
            y=alt.Y(y_sel, type="quantitative"),
            tooltip=["Line", x_sel, y_sel],
        )
    )
    # Combine and render
    st.altair_chart(alt.layer(base, highlight).interactive(),
                    use_container_width=True)

# 8) Download filtered CSV
st.write("---")
st.download_button(
    "Download filtered CSV",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_lines_combined.csv",
    mime="text/csv",
)
