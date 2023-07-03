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

    # 使用Streamlit的两列布局
    col1, col2, col3 = st.beta_columns(3)
    
    # Get data customers_0001
    query_0001 = sql.CUSTOMERS_0001_COUNT_QUERY
    df_0001 = sf.sql_to_dataframe(
        query_0001
    )
    total_customer_0001_count = df_0001.iloc[0, 0]
    if st.session_state.last_customer_0001_number == 0 :
        st.session_state.last_customer_0001_number = total_customer_0001_count
    last_customer_0001_count = st.session_state.last_customer_0001_number
    new_customer_0001_count = total_customer_0001_count - last_customer_0001_count
    with col1:
        metric_value_0001=st.metric(label="Cutomers_0001客户总数", value="{:,}".format(total_customer_0001_count), delta="{:,}".format(new_customer_0001_count))
    # Get data customers_0002
    query_0002 = sql.CUSTOMERS_0002_COUNT_QUERY
    df_0002 = sf.sql_to_dataframe(
        query_0002
    )
    total_customer_0002_count = df_0002.iloc[0, 0]
    if st.session_state.last_customer_0002_number == 0 :
        st.session_state.last_customer_0002_number = total_customer_0002_count
    last_customer_0002_count = st.session_state.last_customer_0002_number
    new_customer_0002_count = total_customer_0002_count - last_customer_0002_count
    with col2:
        metric_value_0002=st.metric(label="Cutomers_0002客户总数", value="{:,}".format(total_customer_0002_count), delta="{:,}".format(new_customer_0002_count))
    # Get data customers_0003
    query_0003 = sql.CUSTOMERS_0003_COUNT_QUERY
    df_0003 = sf.sql_to_dataframe(
        query_0003
    )
    total_customer_0003_count = df_0003.iloc[0, 0]
    if st.session_state.last_customer_0003_number == 0 :
        st.session_state.last_customer_0003_number = total_customer_0003_count
    last_customer_0003_count = st.session_state.last_customer_0003_number
    new_customer_0003_count = total_customer_0003_count - last_customer_0003_count
    with col3:
        metric_value_0003=st.metric(label="Cutomers_0003客户总数", value="{:,}".format(total_customer_0003_count), delta="{:,}".format(new_customer_0003_count))
   
    while True:
        # Wait for 1 seconds
        time.sleep(3)
        # Get data customers_0001
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

        # Get data customers_0002
        df_0002 = sf.sql_to_dataframe(
            query_0002
        )
        total_customer_0002_count = df_0002.iloc[0, 0]
        last_customer_0002_count = st.session_state.last_customer_0002_number
        new_customer_0002_count = total_customer_0002_count - last_customer_0002_count
        st.session_state.last_customer_0002_number = total_customer_0002_count
        # 更新指标的值
        metric_value_0002.value = "{:,}".format(total_customer_0002_count)
        metric_value_0002.delta = "{:,}".format(new_customer_0002_count)

        # Get data customers_0003
        df_0003 = sf.sql_to_dataframe(
            query_0003
        )
        total_customer_0003_count = df_0003.iloc[0, 0]
        last_customer_0003_count = st.session_state.last_customer_0003_number
        new_customer_0003_count = total_customer_0003_count - last_customer_0003_count
        st.session_state.last_customer_0003_number = total_customer_0003_count
        # 更新指标的值
        metric_value_0003.value = "{:,}".format(total_customer_0003_count)
        metric_value_0003.delta = "{:,}".format(new_customer_0003_count)

if __name__ == "__main__":
    main()
