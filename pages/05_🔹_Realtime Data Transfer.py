import plost
import streamlit as st
import time
from utils import charts, gui, processing
from utils import snowflake_connector as sf
from utils import sql as sql

# st.set_page_config(
#     page_title="Usage Insights app - Real time data transfer", page_icon="🔹", layout="wide"
# )

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
    while True:
        # Get data
        query = sql.CUSTOMERS_COUNT_QUERY
        df = sf.sql_to_dataframe(
            query.format(date_from=date_from, date_to=date_to)
        )
        st.table(df)
    
        # query = sql.CUSTOMERS_LIMIT_10
        # df = sf.sql_to_dataframe(
        #     query.format(date_from=date_from, date_to=date_to)
        # )
        # st.table(df)
        # Wait for 2 seconds
        time.sleep(2)
    
        # Rerun the app to refresh the chart
        st.experimental_rerun()
if __name__ == "__main__":
    main()
