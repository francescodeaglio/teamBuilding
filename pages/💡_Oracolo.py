import streamlit as st

from databases.mongo_handler import MongoHandler
from oracles import Oracle1to2, Oracle2to4, Oracle4to8
from utils import set_xtra_large_size

set_xtra_large_size()

st.title("Oracolo")

mongo_handler = MongoHandler()
oracle1to2 = Oracle1to2(mongo_handler.singles_db, mongo_handler.couples_db)
oracle2to4 = Oracle2to4(mongo_handler.couples_db, mongo_handler.quartets_db, mongo_handler.quartets_db)
oracle4to8 = Oracle4to8(mongo_handler.quartets_db, mongo_handler.octets_db)

with st.expander("Forma coppia"):
    oracle1to2.show_page()
with st.expander("Forma quartetto"):
    oracle2to4.show_page()
with st.expander("Forma ottetto"):
    oracle4to8.show_page()
