import streamlit as st
import pymongo



def __main__():
    client = pymongo.MongoClient(
            "mongodb+srv://campoestivo:qVx8khSNIljjfKqw@cluster0.usbb0.mongodb.net/campoestivo?retryWrites=true&w=majority")
    db = client.testOpening
    coppie_db = db["coppie"]

    c1, c2 = st.columns((0.7,0.2))
    c1.title("Checkpointer")
    if c2.button("Aggiorna"):
        st.experimental_rerun()

    st.write("Il checkpointer serve nella seconda fase (quando si gioca in coppie) per tenere traccia del progresso.")

    r = st.selectbox("Scegliere la coppia", get_couples(coppie_db))

    if st.button("Esegui checkpoint"):
        if checkpointa(coppie_db, first=r):
            st.success(f"Coppia {r} checkpointata")
        else:
            st.error(f"Coppia {r} non checkpointata")

def get_couples(coppie):
    res = coppie.find({})
    return [el["nomi"] for el in res if el["attivo"] == True and "awaiting" not in el]


def checkpointa(coppie, first):
    try:
        query_string = {"nomi": first}
        c1 = list(coppie.find(query_string))[0]
        coppie.update_one(c1, {"$set": {"awaiting": True}})
        return True
    except:
        return False


__main__()