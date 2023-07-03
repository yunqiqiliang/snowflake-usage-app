import streamlit as st

st.set_page_config(page_title="Usage Insights app", page_icon="🌀", layout="wide")

from utils import gui

gui.icon("🌀")

# Make sure session state is preserved
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

# Storing The Context
if "last_customer_number" not in st.session_state:
    st.last_customer_number = 0
if "last_customer_0001_number" not in st.session_state:
    st.last_customer_0001_number = 0
if "last_customer_0002_number" not in st.session_state:
    st.last_customer_0002_number = 0
if "last_customer_0003_number" not in st.session_state:
    st.last_customer_0003_number = 0



st.title("Welcome to Qiliang's Snowflake Usage Insights!")
st.sidebar.text(f"Account: {st.secrets.sf_usage_app.account}")
st.sidebar.text(f"Snowflake Role: accountadmin")
st.sidebar.info("Choose a page!")
st.markdown(
    """
This app provides insights on a Snowflake account usage.
### Help you understand Money: Snowflake's charge items.
### Help you understand Data: Data in Snowflake account information schema
### Please enjoy!

👈 Select a page in the sidebar!
    """
)
