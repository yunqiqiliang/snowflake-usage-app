import plost
import streamlit as st
import time
from utils import charts, gui, processing
from utils import snowflake_connector as sf
from utils import sql as sql

from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def get_session(key):
    session_state = SessionState()
    session_id = get_report_ctx().session_id

    if hasattr(st._get_current_session(), '_session_state'):
        # Session state already initialized for this session.
        sessions = st._get_session_info().session_objects
        if key not in sessions[session_id]._session_state:
            # Create a new session state variable if it doesn't exist yet.
            setattr(sessions[session_id]._session_state, key, None)
        session_state = getattr(sessions[session_id]._session_state, key)
    
    else:
        # Initialize a new session.
        session = Server.get_current()._get_session_info(session_id).session
        setattr(session, '_session_state', session_state)
        setattr(session_state, 'key', None)

    return session_state

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
    state = get_session('count')

    if state.count is None:
        state.count = 0

   
    while True:
        # Get data
        query = sql.CUSTOMERS_COUNT_QUERY
        df = sf.sql_to_dataframe(
            query.format(date_from=date_from, date_to=date_to)
        )
        # st.table(df)
        
        
        total_customer_count = df.iloc[0, 0]
        if state.count == 0:
            state.count = total_customer_count
        new_customer_count = total_customer_count - state.count
        
        st.metric(label="客户总数", value="{:,}".format(total_customer_count), delta="{:,}".format(new_customer_count))
        state.count = total_customer_count
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
