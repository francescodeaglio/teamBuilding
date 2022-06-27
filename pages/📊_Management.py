import streamlit as st
import pymongo
from functools import reduce
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots

from counters import counters_persona, counter_stand

client = pymongo.MongoClient(
        "mongodb+srv://campoestivo:qVx8khSNIljjfKqw@cluster0.usbb0.mongodb.net/campoestivo?retryWrites=true&w=majority")
db = client.testOpening

iscritti_db = db.iscritti
coppie_db = db.coppie
quartetti_db = db.quartetti
gestionale_db = db.gestionale
ottetti_db = db.otteti

def get_counter(db):
    L = [(int(el["squadra"]), len(el["ids"]) if "ids" in el else 1) for el in list(db.find({"attivo":True}))]
    counter = {int(el):0 for el in "12345"}
    counter["tot"] = 0
    for sq,cnt in L:
        counter[sq]+=1
        counter["tot"] +=1
    return counter

def pie_faseperfase(iscritti_db, coppie_db, quartetti_db, ottetti_db):
    prima = get_counter(iscritti_db)
    seconda = get_counter(coppie_db)
    terza = get_counter(quartetti_db)
    quarta = get_counter(ottetti_db)

    data = {"singoli": prima, "coppie": seconda, "quartetti": terza, "ottetti": quarta}
    df = pd.DataFrame(data).T

    fig = make_subplots(rows=2, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                                               [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],

                        subplot_titles=["Tutti"] + [f"   Team <b>{team}" for team in list("12345")]
                        )
    fig.update_layout(title="Conteggio fase per fase",
                      title_x=0.5, title_xanchor="center")

    grid = {
        1: (1, 2), 2: (1, 3), 3: (2, 1), 4: (2, 2), 5: (2, 3)
    }

    for i in range(1, 6):
        chart = px.pie(df, values=i, names=df.index, title=f"Squadra **{i}**")
        fig.add_trace(chart.data[0], row=grid[i][0], col=grid[i][1])

    chart = px.pie(df, values="tot", names=df.index, title=f"Squadra **{i}**")
    fig.add_trace(chart.data[0], row=1, col=1)

    for i in range(6):
        fig.layout["annotations"][i]["x"] -= 0.15

    st.plotly_chart(fig)




def __main__():

    c1, c2 = st.columns((0.865,0.135))
    c1.markdown("## Management page")
    c2.text("\n")
    if c2.button("Aggiorna"):
        st.experimental_rerun()
    with st.expander("Conteggio fase per fase"):
        pie_faseperfase(iscritti_db, coppie_db, quartetti_db, ottetti_db)
    st.markdown("### Prima Fase")
    with st.expander("Progressi fase 1 - Individui"):
        counters_persona(fase = 1)
    with st.expander("Progressi fase 1 - Stand"):
        counter_stand()

if __name__ == "__main__":
    __main__()