import plost
import streamlit as st
import time
from utils import snowflake_connector as sf
from utils import clickzetta_connector as cz
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
    st.title("Real time data transfer, From Postgres to Snowflake")
     # --------------------------------
    # ---- Real time data transfer ----
    # ---------------------------------

    st.subheader("Real time data transfer")
    username = st.secrets.lakehouse.username
    password = st.secrets.lakehouse.password
    account = st.secrets.lakehouse.account
    baseurl =st.secrets.lakehouse.baseurl
    database = st.secrets.lakehouse.database
    schema = st.secrets.lakehouse.schema
    virtualcluster =st.secrets.lakehouse.virtualcluster
    clickzettaurl="clickzetta://"+ username + ":"+password+"@"+account+"."+baseurl+"/"+ database +"?schema="+ schema+ "&virtualcluster=" + virtualcluster
    print(f"clickzettaurl: {clickzettaurl}")
    st.subheader(clickzettaurl)

    # 使用Streamlit的两列布局
    col1, col2, col3 = st.columns(3)
    
    # Get data customers_0001
    query_0001 = sql.CUSTOMERS_0001_COUNT_QUERY
    df_0001 = cz.get_lakehouse_queries_data(
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
    df_0002 = cz.get_lakehouse_queries_data(
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
    df_0003 = cz.get_lakehouse_queries_data(
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
        time.sleep(30)
        # Get data customers_0001
        df_0001 = cz.get_lakehouse_queries_data(
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
        df_0002 = cz.get_lakehouse_queries_data(
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
        df_0003 = cz.get_lakehouse_queries_data(
            query_0003
        )
        total_customer_0003_count = df_0003.iloc[0, 0]
        last_customer_0003_count = st.session_state.last_customer_0003_number
        new_customer_0003_count = total_customer_0003_count - last_customer_0003_count
        st.session_state.last_customer_0003_number = total_customer_0003_count
        # 更新指标的值
        metric_value_0003.value = "{:,}".format(total_customer_0003_count)
        metric_value_0003.delta = "{:,}".format(new_customer_0003_count)

        st.experimental_rerun()
        

if __name__ == "__main__":
    main()
