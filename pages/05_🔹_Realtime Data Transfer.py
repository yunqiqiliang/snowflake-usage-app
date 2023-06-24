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
    query = sql.DATA_TRANSFER_QUERY
    df = sf.sql_to_dataframe(
        query.format(date_from=date_from, date_to=date_to)
    )



if __name__ == "__main__":
    main()
