import plost
import streamlit as st

st.set_page_config(
    page_title="Usage Insights app - Real time data transfer", page_icon="🔹", layout="wide"
)

from utils import charts, gui, processing
from utils import snowflake_connector as sf
from utils import sql as sql


def main():

    # Date selector widget
    with st.sidebar:
        date_from, date_to = gui.date_selector()

    # Header
    # gui.icon("🔹")
    st.title("Real time data transfer, From Postgres to Snowflake")
     # --------------------------------
    # ---- Real time data transfer ----
    # ---------------------------------

    gui.space(1)
    st.subheader("Real time data transfer")
    # Get data
    df = sf.sql_to_dataframe(
        query.format(date_from=date_from, date_to=date_to)
    )

    

    # ----------------------
    # ---- Service type ----
    # ----------------------

    gui.space(1)
    st.subheader("Service type")

    # Get data
    query = sql.CONSUMPTION_PER_SERVICE_TYPE_QUERY
    df = sf.sql_to_dataframe(
        query.format(date_from=date_from, date_to=date_to)
    )

    # Add filtering widget per Service type
    all_values = df["SERVICE_TYPE"].unique().tolist()
    selected_value = st.selectbox(
        "Choose service type",
        ["All"] + all_values,
        0,
    )

    if selected_value == "All":
        selected_value = all_values
    else:
        selected_value = [selected_value]

    # Filter df accordingly
    df = df[df["SERVICE_TYPE"].isin(selected_value)]

    # Get consumption
    consumption = int(df["CREDITS_USED"].sum())

    if df.empty:
        st.caption("No data found.")
    elif consumption == 0:
        st.caption("No consumption found.")
    else:
        # Sum of credits used
        credits_used_html = gui.underline(
            text=gui.pretty_print_credits(consumption),
        )
        credits_used_html += " were used"

        gui.space(1)
        st.write(credits_used_html, unsafe_allow_html=True)

        gui.space(1)
        gui.subsubheader(
            "**Compute** spend over time",
            "Aggregated by day",
        )

        # Resample by day
        df_resampled = processing.resample_by_day(
            df,
            date_column="START_TIME",
        )

        # Bar chart
        bar_chart = charts.get_bar_chart(
            df=df_resampled,
            date_column="START_TIME",
            value_column="CREDITS_USED",
        )

        st.altair_chart(bar_chart, use_container_width=True)

        # Group by
        agg_config = {"CREDITS_USED": "sum"}
        df_grouped = (
            df.groupby(["NAME", "SERVICE_TYPE"]).agg(agg_config).reset_index()
        )

        # Sort and pretty print credits
        df_grouped_top_10 = df_grouped.sort_values(
            by="CREDITS_USED", ascending=False
        ).head(10)

        df_grouped_top_10["CREDITS_USED"] = df_grouped_top_10[
            "CREDITS_USED"
        ].apply(gui.pretty_print_credits)

        gui.subsubheader(
            "**Compute** spend",
            " Grouped by NAME",
            "Top 10",
        )

        st.dataframe(
            gui.dataframe_with_podium(
                df_grouped_top_10,
            )[["NAME", "SERVICE_TYPE", "CREDITS_USED"]],
            width=600,
        )

        gui.space(1)
        gui.hbar()

    # -------------------
    # ---- Warehouse ----
    # -------------------

    st.subheader("Warehouse")

    # Get data
    warehouse_usage_hourly = sf.sql_to_dataframe(
        sql.WAREHOUSE_USAGE_HOURLY.format(
            date_from=date_from,
            date_to=date_to,
        )
    )

    # Add filtering widget per Warehouse name
    warehouses = warehouse_usage_hourly.WAREHOUSE_NAME.unique()
    selected_warehouse = st.selectbox(
        "Choosed warehouse",
        warehouses.tolist(),
    )

    # Filter accordingly
    warehouse_usage_hourly_filtered = warehouse_usage_hourly[
        warehouse_usage_hourly.WAREHOUSE_NAME.eq(selected_warehouse)
    ]

    # Resample so that all the period has data (fill with 0 if needed)
    warehouse_usage_hourly_filtered = processing.resample_date_period(
        warehouse_usage_hourly_filtered,
        date_from,
        date_to,
        value_column="CREDITS_USED_COMPUTE",
    )

    gui.subsubheader("Time-histogram of **warehouse usage**")

    plost.time_hist(
        data=warehouse_usage_hourly_filtered,
        date="START_TIME",
        x_unit="day",
        y_unit="hours",
        color={
            "field": "CREDITS_USED_COMPUTE",
            "scale": {
                "scheme": charts.ALTAIR_SCHEME,
            },
        },
        aggregate=None,
        legend=None,
    )



if __name__ == "__main__":
    main()
