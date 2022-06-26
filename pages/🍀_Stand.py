import streamlit as st

from stand_quartetti import frontend_quartetti
from utils import *
from stand_individui import *
import pymongo

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

if "selected_stand" not in st.session_state:
    st.write("### Selezionare lo stand")
    st.session_state["selected_stand"] = st.selectbox("Seleziona il tuo stand", get_labels_stands())
    if st.button("Conferma"):
        st.experimental_rerun()
else:
    client = pymongo.MongoClient(
        "mongodb+srv://campoestivo:qVx8khSNIljjfKqw@cluster0.usbb0.mongodb.net/campoestivo?retryWrites=true&w=majority")
    db = client.testOpening
    singoli_db = db["iscritti"]
    coppie_db = db["coppie"]
    quartetti_db = db["quartetti"]
    ottetti_db = db["ottetti"]

    stand = st.session_state["selected_stand"]
    st.title(f"Stand: {stand}")
    with st.expander("Cambia stand"):
        st.session_state["selected_stand"] = st.selectbox("Seleziona il nuovo stand", get_labels_stands())
        if st.button("Conferma"):
            st.experimental_rerun()

    with st.expander("Prima fase: da singoli a coppie"):
        frontend_individui(stand, singoli_db)

    with st.expander("Terza fase: da quartetti a ottetti"):
        frontend_quartetti(stand, singoli_db, coppie_db, quartetti_db)

