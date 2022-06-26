import streamlit as st

def get_couples(coppie):
    res = coppie.find({})
    return [el["nomi"] for el in res if el["attivo"] == True]


def sestetto(gestionale_db, coppie_db, elemento):
    query_string = {"nomi": elemento}
    c1 = list(coppie_db.find(query_string))[0]

    squadra = c1["squadra"]

    res = list(gestionale_db.find({
        "fase" : "quartetti",
        "squadra" : squadra
    }))

    if len(res) == 0:
        return False
    else:
        return False if res[0]["counter"] != 3 else True


def success_sestetto(first, second, third, coppie_db, quartetti_db, gestionale_db):
    query_string = {"nomi": first}
    res = list(coppie_db.find(query_string))
    coppie_db.update_one(res[0], {"$set": {"attivo": False}})

    query_string = {"nomi": second}
    res1 = list(coppie_db.find(query_string))
    coppie_db.update_one(res1[0], {"$set": {"attivo": False}})

    query_string = {"nomi": third}
    res2 = list(coppie_db.find(query_string))
    coppie_db.update_one(res2[0], {"$set": {"attivo": False}})


    quartetto = {
        "membri": res[0]["nomicognomi"] + res1[0]["nomicognomi"] + res2[0]["nomicognomi"],
        "ids": res[0]["ids"] + res1[0]["ids"] + res2[0]["ids"],
        "attivo": True,
        "squadra": res2[0]["squadra"],
        "nomi": f'{res[0]["nomi"]} - {res1[0]["nomi"]} - {res2[0]["nomi"]}',
        "available": True
    }

    if check_preaccoppiamento([res[0], res1[0], res2[0]]):
        altri = mantieni_accoppiamento([res[0], res1[0], res2[0]], quartetti_db)
        quartetto["altri"] = altri
        quartetto["available"] = False

    quartetti_db.insert_one(quartetto)

    squadra = res[0]["squadra"]

    res = list(gestionale_db.find({
        "fase": "quartetti",
        "squadra": squadra
    }))

    if len(res) == 0:
        gestionale_db.insert_one(
            {
                "fase": "quartetti",
                "squadra": squadra,
                "counter": 1
            }
        )
    else:
        gestionale_db.update_one(res[0], {"$set": {
            "counter": int(res[0]["counter"]) + 1
        }})


def frontend_oracolo2to4(coppie_db, quartetti_db, gestionale_db):
    couples = get_couples(coppie_db)

    print(len(couples))
    if len(couples) == 0:
        st.write("Nessuna coppia in questa fase")
        return
    with st.form("Ricerca oracolo coppie"):

        first = st.selectbox("Prima coppia", couples)
        second = st.selectbox("Seconda coppia", couples[::-1])


        submitted = st.form_submit_button("Forma")
        if submitted and first != second:
            if is_quartetto(coppie_db, first, second):

                #qua bisogna gestire il caso particolare in cui l'ultimo quartetto è in realtà un quintetto
                if not sestetto(gestionale_db, coppie_db, first):
                    success(first, second, coppie_db, quartetti_db, gestionale_db)
                    st.success("Quartetto formato!\n Avanzate alla prossima fase!")
                else:
                    st.warning("Siete nella stessa squadra ma formerete un sestetto. Aspettate l'ultima coppia della vostra squadra.")
                    st.write("Se invece è disponibile una terza coppia potete provare a inserirla per vedere se siete nella stessa squadra")
                    third = st.selectbox("Terza coppia", couples[::-1])


                    if is_quartetto(coppie_db, first, third) and first != third and second != third:
                            #tanto primo e secondo siam sicuri che siano uguali
                            success_sestetto(first, second, third, coppie_db, quartetti_db, gestionale_db)
                            st.success("Sestetto formato!\n Avanzate alla prossima fase!")
                    else:
                            st.error("Queste due coppie non appartengono alla stessa squadra o non sono tre coppie diverse:(")
                            st.write("Assicurarsi che i tre selectbox contengano tre coppie diverse")

            else:
                st.error("Queste due coppie non appartengono alla stessa squadra :(")

def is_quartetto(coppie, first, second):
    try:
        query_string = {"nomi": first}
        c1 = list(coppie.find(query_string))[0]
        coppie.update_one(c1, {"$set": {"awaiting": True}})

        query_string = {"nomi": second}
        c2 = list(coppie.find(query_string))[0]
        coppie.update_one(c2, {"$set": {"awaiting": True}})

        return c1["squadra"] == c2["squadra"]
    except:
        return False

def success(c1, c2, coppie, quartetti, gestionale):

    query_string = {"nomi": c1}
    res = list(coppie.find(query_string))
    coppie.update_one(res[0], {"$set": {"attivo": False}})

    query_string = {"nomi": c2}
    res2 = list(coppie.find(query_string))
    coppie.update_one(res2[0], {"$set": {"attivo": False}})

    quartetto = {
        "membri": res[0]["nomicognomi"] + res2[0]["nomicognomi"],
        "ids": res[0]["ids"] + res2[0]["ids"],
        "attivo": True,
        "squadra": res2[0]["squadra"],
        "nomi" : f'{res[0]["nomi"]} - {res2[0]["nomi"]}',
        "available":True
    }
    if check_preaccoppiamento([res[0], res2[0]]):
        altri = mantieni_accoppiamento([res[0], res2[0]], quartetti)
        quartetto["altri"] = altri
        quartetto["available"] = False

    quartetti.insert_one(quartetto)

    squadra = res[0]["squadra"]

    res = list(gestionale.find({
        "fase": "quartetti",
        "squadra": squadra
    }))

    if len(res) == 0:
        gestionale.insert_one(
            {
                "fase": "quartetti",
                "squadra": squadra,
                "counter": 1
            }
        )
    else:
        gestionale.update_one(res[0], {"$set": {
            "counter": int(res[0]["counter"]) + 1
        }})

def check_preaccoppiamento(members):
    for member in members:
        if member["available"] == False:
            return True
    return False

def mantieni_accoppiamento(members, quartetti_db, ):
    for member in members:
        if member["available"] == False:
            nomi = member["nomi"]
            break

    for quartetto in quartetti_db.find({}):
        if "altri" in quartetto and quartetto["altri"]["nomi_coppia"] == nomi:

            return {
                "tipo": "quartetto",
                "nomi_quartetto":quartetto["nomi"],
                "ids":quartetto["ids"]
            }




