import plost
import streamlit as st
import time
from utils import charts, gui, processing
from utils import snowflake_connector as sf
from utils import sql as sql

# Storing The Context
if "last_customer_number" not in st.session_state:
    st.session_state.last_customer_number = 0
if "last_customer_0001_number" not in st.session_state:
    st.session_state.last_customer_0001_number = 0
if "last_customer_0002_number" not in st.session_state:
    st.session_state.last_customer_0002_number = 0
if "last_customer_0003_number" not in st.session_state:
    st.session_state.last_customer_0003_number = 0

# st.set_page_config(
#     page_title="Usage Insights app - Real time data transfer", page_icon="🔹", layout="wide"
# )
def main():

    # Header
    # gui.icon("🔹")
    st.title("Real time data transfer, From Postgres to Snowflake")
     # --------------------------------
    # ---- Real time data transfer ----
    # ---------------------------------

    gui.space(1)
    st.subheader("Real time data transfer")
    # Get data
    query_0001 = sql.CUSTOMERS_0001_COUNT_QUERY
    df_0001 = sf.sql_to_dataframe(
        query_0001
    )
    total_customer_0001_count = df_0001.iloc[0, 0]
    last_customer_0001_count = 0
    new_customer_0001_count = 0
    if st.session_state.last_customer_0001_number == 0 :
        st.session_state.last_customer_0001_number = total_customer_0001_count
    last_customer_0001_count = st.session_state.last_customer_0001_number
    new_customer_0001_count = total_customer_0001_count - last_customer_0001_count
    metric_value_0001=st.metric(label="Cutomers_0001客户总数", value="{:,}".format(total_customer_0001_count), delta="{:,}".format(new_customer_0001_count))
   
    while True:
        # Wait for 1 seconds
        time.sleep(1)
        # Get data
        query_0001 = sql.CUSTOMERS_0001_COUNT_QUERY
        df_0001 = sf.sql_to_dataframe(
            query_0001
        )
        total_customer_0001_count = df_0001.iloc[0, 0]
        last_customer_0001_count = st.session_state.last_customer_0001_number
        new_customer_0001_count = total_customer_0001_count - last_customer_0001_count
        st.session_state.last_customer_0001_number = total_customer_0001_count
        # 更新指标的值
        metric_value_0001.value = "{:,}".format(total_customer_0001_count)
        metric_value_0001.delta = "{:,}".format(new_customer_0001_count)
        
    
        # Rerun the app to refresh the chart
        # st.experimental_rerun()
if __name__ == "__main__":
    main()
