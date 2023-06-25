import plost
import streamlit as st
import time
from utils import charts, gui, processing
from utils import snowflake_connector as sf
from utils import sql as sql
from streamlit.hashing import _CodeHasher

# st.set_page_config(
#     page_title="Usage Insights app - Real time data transfer", page_icon="🔹", layout="wide"
# )
def get_state(hash_funcs=None):
    return st.session_state


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

    last_customer_count = get_state()

    if 'count' not in state:
        last_customer_count.count = 0
   
    while True:
        # Get data
        query = sql.CUSTOMERS_COUNT_QUERY
        df = sf.sql_to_dataframe(
            query.format(date_from=date_from, date_to=date_to)
        )
        # st.table(df)
        
        
        total_customer_count = df.iloc[0, 0]
        if last_customer_count.count == 0:
            last_customer_count.count = total_customer_count
        new_customer_count = total_customer_count - last_customer_count.count
        
        st.metric(label="客户总数", value="{:,}".format(total_customer_count), delta="{:,}".format(new_customer_count))
        last_customer_count.count = total_customer_count
        # query = sql.CUSTOMERS_LIMIT_10
        # df = sf.sql_to_dataframe(
        #     query.format(date_from=date_from, date_to=date_to)
        # )
        # st.table(df)
        # Wait for 10 seconds
        time.sleep(10)
    
        # Rerun the app to refresh the chart
        st.experimental_rerun()
if __name__ == "__main__":
    main()
