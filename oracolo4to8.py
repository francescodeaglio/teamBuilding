import streamlit as st

def frontend_oracolo4to8(quartetti_db, ottetti_db):
    forma_ottetto(quartetti_db, ottetti_db)

def forma_ottetto(quartetti_db, ottetti_db):
    with st.form("Ricerca oracolo - Ottetti"):
        st.write("Inserisci il codice di un membro di ognuno dei due quartetti")
        c1 = st.text_input('Inserisci il codice di un membro del primo quartetto')
        c2 = st.text_input('Inserisci il codice di un membro del secondo quartetto')

        submitted = st.form_submit_button("Cerca")
        if submitted:
            ricerca_oracolo(quartetti_db, c1, c2, ottetti_db)

def ricerca_oracolo(quartetti_db, c1, c2, ottetti_db):
    res = list(quartetti_db.find({}))

    for el in res:

        if (int(c1) in [int(id) for id in el["ids"]] and int(c2) in [int(id) for id in el["altri"]["ids"]])\
                or (int(c2) in [int(id) for id in el["ids"]] and int(c1) in [int(id) for id in el["altri"]["ids"]]):
            success(c1, c2, quartetti_db, ottetti_db)
            st.success("It's a match!")
            return

    st.error("Non siete insieme :(\t Continuate a cercare!")

def success(c1, c2, quartetti_db, ottetti_db):

    res = list(quartetti_db.find({}))

    primo, secondo = None, None
    for el in res:
        if int(c1) in [int(x) for x in el["ids"]]:
            primo = el
        if int(c2) in [int(x) for x in el["ids"]]:
            secondo = el

    quartetti_db.update_one(primo, {"$set": {"attivo": False}})
    quartetti_db.update_one(secondo, {"$set": {"attivo": False}})

    ottetto = {

        "membri" : primo["membri"] + secondo["membri"],
        "ids": primo["ids"] + secondo["ids"],
        "attivo": True,
        "squadra": primo["squadra"],
        "nomi" : f'{primo["nomi"]} - {secondo["nomi"]}',
        "available":True
    }

    ottetti_db.insert_one(ottetto)

