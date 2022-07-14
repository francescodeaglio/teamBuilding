import streamlit as st
from utils import *
import pymongo

def frontend_individui(stand, individui_db):
    stand_letter = stand.split("-")[0].strip()
    st.markdown(f"###### Descrizione stand\n\n {get_descrizione_individui()[stand_letter]}")

    with st.form("Ricerca stand"):

        if "cached_ids" not in st.session_state:
            partecipants = get_all_names(individui_db)
            st.session_state["cached_ids"] = partecipants
        else:
            partecipants = st.session_state["cached_ids"]

        partecipant = st.selectbox("Cerca il partecipante", partecipants)
        my_id, others_id = partecipants[partecipant]

        submitted = st.form_submit_button("Cerca")
        if submitted:
            stand_status_update(individui_db, my_id, others_id, stand_letter)

def get_all_names(partecipants):
    """
    Function to get the names of all partecipants (used in the search bar)
    :param partecipants: mongodb instance
    :return: dict of tuples key = first last, value = (my_id, other's id)
    """
    res = list(partecipants.find({}))
    ret = {}
    for el in res:
        first = el["Nome"]
        last = el["Cognome"]
        if "coppia" in el:
            ret[f"{first} {last}"] = (int(el["Id"]), int(el["coppia"]["Id"]))
    return ret


def stand_status_update(col, my_id, others_id, stand):
    """
    Function to store the completion of a stand by a given player
    :param col: mongoDb collection
    :param my_id: id of the player that has completed the game
    :param others_id: id of the other player in the couple
    :param stand: stand letter (A, B...)
    :return: void
    """
    res = list(col.find({"Id": my_id}))

    if res[0]["stand_visitati"][stand]:
        st.error(f"{res[0]['nomecognome']} ha già visitato questo stand!")
    else:
        col.update_one(res[0], {"$set": {"stand_visitati." + stand: True}})
        st.success("Consegna la busta numero " + str(others_id))
