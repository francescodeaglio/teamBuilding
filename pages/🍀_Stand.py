from databases.mongo_handler import MongoHandler
from stands.stand_quartets import StandQuartets
from stands.stand_singles import StandSingles
import streamlit as st
from utils import get_labels_stands, set_xtra_large_size

set_xtra_large_size()

if "selected_stand" not in st.session_state:
    st.write("### Selezionare lo stand")
    st.session_state["selected_stand"] = st.selectbox("Seleziona il tuo stand", get_labels_stands())
    if st.button("Conferma"):
        st.rerun()
else:
    mongo_handler = MongoHandler()

    stand = st.session_state["selected_stand"]
    st.title(f"Stand: {stand}")
    with st.expander("Cambia stand"):
        st.session_state["selected_stand"] = st.selectbox("Seleziona il nuovo stand", get_labels_stands())
        if st.button("Conferma"):
            st.rerun()

    with st.expander("Prima fase: da singoli a coppie"):
        StandSingles(stand,
                     mongo_handler.singles_db
                     ).show_page()

    with st.expander("Terza fase: da quartetti a ottetti"):
        StandQuartets(stand,
                      mongo_handler.singles_db,
                      mongo_handler.couples_db,
                      mongo_handler.quartets_db
                      ).show_page()
