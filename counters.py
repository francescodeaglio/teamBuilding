import pymongo
import pandas as pd
import streamlit as st
import plotly.express as px

def conta_visitati(elenco):
    ret = {}
    for persona in elenco:
        conta = 0
        for stand in persona["stand_visitati"]:
            if persona["stand_visitati"][stand] == True:
                conta+=1
        ret[persona["nomecognome"]] = {"Stand Visitati":conta, "Squadra":str(int(persona["squadra"]))}
    return ret


def counters_persona(fase = 1):
    client = pymongo.MongoClient(
        "mongodb+srv://campoestivo:qVx8khSNIljjfKqw@cluster0.usbb0.mongodb.net/campoestivo?retryWrites=true&w=majority")
    db = client.testOpening
    iscritti_db = db.iscritti
    if fase == 1:
        elenco = list(iscritti_db.find({"attivo":True}, {"stand_visitati": True, "nomecognome": True, "_id": False, "squadra": True}))
        counter = conta_visitati(elenco)
        data = pd.DataFrame(counter).T
        data["Nome"] = data.index
        fig = px.bar(data, x="Stand Visitati", y="Nome", color="Squadra", orientation='h', title="<b>Stand visitati")
        fig.update_layout(height=1500, title_x=0.5)
        st.plotly_chart(fig)

def conta_stand(elenco):
    stands = [{"stand":stand, "squadra":sq, "count":0} for sq in "12345" for stand in "ABCDEFGHIL"]
    for persona in elenco:
        for s in persona["stand_visitati"]:
            if persona["stand_visitati"][s]:
                for x in stands:
                    if x["squadra"] == str(int(persona["squadra"])) and x["stand"] == s:
                        x["count"]+=1
    return stands

def counter_stand():
    client = pymongo.MongoClient(
        "mongodb+srv://campoestivo:qVx8khSNIljjfKqw@cluster0.usbb0.mongodb.net/campoestivo?retryWrites=true&w=majority")
    db = client.testOpening
    iscritti_db = db.iscritti
    elenco = list(iscritti_db.find({"attivo": True},
                                   {"stand_visitati": True, "nomecognome": True, "_id": False, "squadra": True}))
    data = conta_stand(elenco)
    data = pd.DataFrame(data)
    data = data.sort_values(by="stand")
    fig = px.bar(data, x="count", y="stand", color="squadra", orientation='h', title="<b>Stand visitati")
    fig.update_layout(height=500, title_x=0.5)
    st.plotly_chart(fig)

