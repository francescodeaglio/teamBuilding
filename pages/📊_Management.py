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


def attivi_terza_fase(quartetti_db):
    attivi = list(quartetti_db.find({}))
    elenco = {squadra: [] for squadra in "12345"}
    for membro in attivi:
        s = f'Quartetto **{membro["nomi"]}**'
        if "altri" not in membro:
            s += " non è ancora stato definito l'altro quartetto"
        else:
            if membro["altri"]["tipo"] == "quartetto":
                s += f' stanno cercando **{membro["altri"]["nomi_quartetto"]}**'
            else:
                s += f' per ora stanno cercando **{membro["altri"]["nomi_coppia"]}**'
        elenco[str(int(membro["squadra"]))].append(s)

    for squadra in sorted(list(elenco.keys())):
        st.write("#### Squadra: " + squadra)
        if len(elenco[squadra]) == 0:
            st.write("Nessun quartetto attivo")
        else:
            st.markdown("\n\n".join(elenco[squadra]))


def attivi_quarta_fase(ottetti_db):
    attivi = list(ottetti_db.find({}))
    elenco = {squadra: [] for squadra in "12345"}
    for membro in attivi:
        s = f'Ottetto **{membro["nomi"]}**'
        elenco[str(int(membro["squadra"]))].append(s)

    for squadra in sorted(list(elenco.keys())):
        st.write("#### Squadra: " + squadra)
        if len(elenco[squadra]) == 0:
            st.write("Nessun ottetto completato")
        else:
            st.markdown("\n".join(elenco[squadra]))


def ricerca(iscritti_db, coppie_db, quartetti_db, ottetti_db):
    nome = st.selectbox("Seleziona il nome", get_all_names(iscritti_db).keys())

    info = iscritti_db.find_one({"nomecognome": nome})
    title = nome + f' (Squadra : {int(info["squadra"])}, Id : {int(info["Id"])})'
    st.write("#### "+ title)

    strings = []

    # prima fase
    string = f'**Fase 1**: {nome} {"è attivo" if info["attivo"] == True else "non è attivo"}\n\n'
    stands = [x for x in info["stand_visitati"] if info["stand_visitati"][x] == True]
    string += f'Ha completato {"gli stand " + "-".join(stands) if len(stands) > 0 else "nessuno stand"} e deve cercare {info["coppia"]["nomecognome"]} (id = {int(info["coppia"]["Id"])})'
    strings.append(string)
    # seconda fase
    info = coppie_db.find_one({"nomicognomi": nome})
    if info is None:
        string = f'**Fase 2**: {nome} non è attivo'
    else:
        string = f'**Fase 2**: {nome} {"è attivo" if info["attivo"] == True else "non è attivo"}'
        if info["awaiting"] == True and info["attivo"] == True:
            string += "\n\nAl momento sta aspettando una coppia disponibile della sua squadra"
    strings.append(string)
    # terza fase
    info = quartetti_db.find_one({"membri": nome})
    if info is None:
        string = f'**Fase 3**: {nome} non è attivo'
    else:
        string = f'**Fase 3**: {nome} {"è attivo" if info["attivo"] == True else "non è attivo"}\n\n'
        string += f'Fa parte del quartetto *{info["nomi"]}* i cui id sono rispettivamente {info["ids"]}\n\n'
        if "altri" not in info:
            string += "Non è ancora stato definito l'altro quartetto"
        else:
            if info["altri"]["tipo"] == "quartetto":
                string += f'Stanno cercando *{info["altri"]["nomi_quartetto"]}* i cui id sono rispettivamente {info["altri"]["ids"]}'
            else:
                string += f' per ora stanno cercando *{info["altri"]["nomi_coppia"]}* i cui id sono rispettivamente {info["altri"]["ids"]}'
    strings.append(string)
    # quarta fase
    info = ottetti_db.find_one({"nomicognomi": nome})
    if info is None:
        string = f'**Fase 4**: {nome} non è attivo'
    else:
        string = f'**Fase 4**: {nome} {"è attivo" if info["attivo"] == True else "non è attivo"}\n\n'
        string += f'Fa parte dell ottetto *{info["nomi"]}*'
    strings.append(string)
    out = "\n\n".join(strings)
    st.markdown(out)

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
            ret[f"{el['nomecognome']}"] = (int(el["Id"]), int(el["coppia"]["Id"]))
    return ret


def __main__():

    c1, c2 = st.columns((0.865,0.135))
    c1.markdown("## Management page")
    c2.text("\n")
    if c2.button("Aggiorna"):
        st.experimental_rerun()
    with st.expander("Conteggio fase per fase"):
        pie_faseperfase(iscritti_db, coppie_db, quartetti_db, ottetti_db)
    with st.expander("Ricerca partecipante"):
        ricerca(iscritti_db, coppie_db, quartetti_db, ottetti_db)
    st.markdown("### Prima Fase")
    with st.expander("Progressi Individui"):
        counters_persona(fase = 1)
    with st.expander("Progressi Stand"):
        counter_stand()
    st.markdown("### Seconda fase")
    with st.expander("Awaiting"):
        st.code("Awaiting = persone che han completato uno stand e stanno aspettando l'altra coppia della propria squadra")
        awaiting = list(coppie_db.find({"awaiting": True, "attivo": True}))
        st.write(
            "\n".join([f'Squadra {int(x["squadra"])} : {x["nomi"]}' for x in awaiting])
        )
    st.markdown("### Terza fase")
    with st.expander("Attivi"):
        st.error("TODO: aggiungere filtro attivi nella query. Tolto per debug")
        attivi_terza_fase(quartetti_db)
    st.markdown("### Quarta fase")
    with st.expander("Attivi"):
        attivi_quarta_fase(ottetti_db)


if __name__ == "__main__":
    __main__()