import streamlit as st

def frontend_oracolo1to2(singoli_db, coppie_db):
    forma_coppia(singoli_db, coppie_db)

def forma_coppia(singoli, coppie):
    with st.form("Ricerca oracolo"):
        st.write("Inserisci i due codici cercati")
        c1 = st.text_input('Inserisci il primo codice')
        c2 = st.text_input('Inserisci secondo codice')

        submitted = st.form_submit_button("Cerca")
        if submitted:
            ricerca_oracolo(singoli, c1, c2, coppie)

def ricerca_oracolo(singoli, c1, c2, coppie):
    query_string = {"Id":int(c1)}
    res = list(singoli.find(query_string))

    if len(res) == 0:
        st.warning("Nessun risultato, il primo numero è inesistente")
    else:
        numero = res[0]["coppia"]["Id"]
        if int(c2) == int(numero):
            success(c1,c2, singoli, coppie)
            st.success("It's a match!")
        else:
            st.error("Non siete insieme :(\t Continuate a cercare!")

def success(c1, c2, singoli, coppie):

    query_string = {"Id": int(c1)}
    res = list(singoli.find(query_string))
    singoli.update_one(res[0], {"$set": {"attivo": False}})

    query_string = {"Id": int(c2)}
    res2 = list(singoli.find(query_string))
    singoli.update_one(res2[0], {"$set": {"attivo": False}})

    coppia = {

        "nomicognomi" : [res[0]["nomecognome"], res2[0]["nomecognome"]],
        "ids": [res[0]["Id"], res2[0]["Id"]],
        "attivo": True,
        "squadra": res2[0]["squadra"],
        "nomi" : f'{res[0]["nomecognome"]} - {res2[0]["nomecognome"]}',
        "available":True
    }

    coppie.insert_one(coppia)

