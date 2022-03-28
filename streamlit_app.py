import streamlit as st
import psycopg2
from urllib.parse import urlparse
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    result = urlparse(st.secrets["postgres"]["connstr"])
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    return psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname,
        port = port
    )
conn = init_connection()
# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
rows = run_query("SELECT * from countries;")
# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
