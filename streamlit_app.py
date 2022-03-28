# streamlit_app.py

import streamlit as st
from supabase import create_client, Client

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    url    = st.secrets["supabase"]["supabase_url"]
    key    = st.secrets["supabase"]["supabase_key"]
    return create_client(url, key)

supabase = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query():
    return supabase.table("countries").select("*").execute()

# Results are returned as [...results]
rows = run_query()[0]

# Print results.
for row in rows:
    st.write(f"Name of country is {row.name} and it is on:{row.continent}:")
