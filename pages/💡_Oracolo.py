import streamlit as st
import pymongo

from Oracle1to2 import Oracle1to2
from oracolo2to4 import frontend_oracolo2to4
from oracolo4to8 import frontend_oracolo4to8

st.markdown(
        """
    <style>
    .streamlit-expanderHeader {
        font-size: x-large;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

st.title("Oracolo")
client = pymongo.MongoClient(
        "mongodb+srv://campoestivo:qVx8khSNIljjfKqw@cluster0.usbb0.mongodb.net/campoestivo?retryWrites=true&w=majority")
db = client.testOpening
singoli_db = db["iscritti"]
coppie_db = db["coppie"]
quartetti_db = db["quartetti"]
ottetti_db = db["otteti"]
gestionale_db = db["gestionale"]


oracle1to2 = Oracle1to2(singoli_db, coppie_db)

with st.expander("Forma coppia"):
    oracle1to2.show_page()
with st.expander("Forma quartetto"):
    frontend_oracolo2to4(coppie_db, quartetti_db, gestionale_db)

with st.expander("Forma ottetto"):
    frontend_oracolo4to8(quartetti_db, ottetti_db)


