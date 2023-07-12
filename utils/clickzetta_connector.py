import streamlit as st
import pandas as pd

username = st.secrets.lakehouse.username
password = st.secrets.lakehouse.password
account = st.secrets.lakehouse.account
baseurl =st.secrets.lakehouse.baseurl
database = st.secrets.lakehouse.database
schema = st.secrets.lakehouse.schema
virtualcluster =st.secrets.lakehouse.virtualcluster
clickzettaurl="clickzetta://"+ username + ":"+password+"@"+account+"."+baseurl+"/"+ database +"?schema="+ schema+ "&virtualcluster=" + virtualcluster
lakehouse_conn = st.experimental_connection(
  "clickzetta",
  type="sql",
  url= clickzettaurl
)
TIME_TO_LIVE = 0 * 0 * 0  # 6 hours caching
@st.experimental_memo(ttl=TIME_TO_LIVE)
def get_lakehouse_queries_data(sql_query: str) -> (pd.DataFrame, str, str):
    data = pd.DataFrame()
    error_code = ""
    error_reason = ""
    print(f"clickzettaurl: {clickzettaurl}")
    try:
        # 执行 SQL 查询
        data = lakehouse_conn.query(sql_query)
        # 如果查询成功，则对 DataFrame 进行进一步处理
        return data, error_code, error_reason
    except Exception as e:
        # 如果查询失败，则打印错误代码和错误原因，并进行相应处理
#         print(f"Error code: {e.args[0]}")
#         print(f"Error reason: {e.args[1]}")
#         error_code = e.args[0]
#         error_reason = e.args[1]
        return data, error_code, error_reason
