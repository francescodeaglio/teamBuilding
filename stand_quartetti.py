import streamlit as st
from utils import *

def frontend_quartetti(stand, singoli_db, coppie_db, quartetti_db):
    stand_letter = stand.split("-")[0].strip()
    st.markdown(f"###### Descrizione stand\n\n {get_descrizione_quartetti()[stand_letter]}")

    with st.form("Ricerca stand - quartetti"):

        partecipants = get_all_quartets(quartetti_db)

        nomi = st.selectbox("Cerca il quartetto", partecipants)

        submitted = st.form_submit_button("Cerca")
        if submitted:
            stand_status_update_4(singoli_db, coppie_db, quartetti_db, nomi, stand_letter)


def get_all_quartets(col):
    res = list(col.find({}))
    ret = []
    for el in res:
        ret.append(el["nomi"])
    return ret

def find_suitable(singoli, ids, stand):
    print(ids)
    for id in ids:
        res = singoli.find({"Id":id})[0]
        if res["stand_visitati"][stand] == False:
            singoli.update_one(res, {"$set": {"stand_visitati." + stand: True}})
            return id
    return None


def stand_status_update_4(singoli, coppie, quartetti, nomi, selected_stand):
    #qua è un po' più complesso perchè potrebbe non esserci un altro quartetto di quella squadra

    players = quartetti.find({"nomi":nomi})[0]

    #controlliamo se abbiamo già assegnato un altro quartetto
    if "altri" in players:
        if players["altri"]["tipo"] == "coppia":
            #controlliamo se nel mentre son diventati un quartetto
            r = coppie.find({"nomi":players["altri"]["nomi_coppia"]})[0]
            if r["attivo"] == False:
                #cerco il corrispondente quartetto
                for q in quartetti.find({}):
                    if players["altri"]["nomi_coppia"] in q["nomi"]:
                        new_q = q
                        break

                #e lo aggiorno con le info per i quartetti
                quartetti.update_one(players, {"$set":{
                    "altri":{
                        "tipo" : "quartetto",
                        "nomi_quartetto": new_q["nomi"],
                        "ids":new_q["ids"]
                    }
                }})
                quartetti.update_one(new_q, {"$set": {
                    "altri": {
                        "tipo": "quartetto",
                        "nomi_quartetto": players["nomi"],
                        "ids": players["ids"]
                    }
                }})

                ids = new_q["ids"]
            else:
                ids = r["ids"]
        else:
            ids = players["altri"]["ids"]

        busta = find_suitable(singoli, ids, selected_stand)

        if busta is not None:
            st.success(f"Consegna la busta numero {int(busta)}")
        else:
            st.error("Non rimane nessuna busta dell'altro quartetto in questo stand")
        return

    #altrimenti dobbiamo assegnarlo
    others_quartetti = list(quartetti.find({"squadra":players["squadra"], "available":True, "nomi":{"$ne":nomi}}))

    if len(others_quartetti) == 0:
        #non c'è nessun'altro quartetto di questa squadra in fase3
        #vediamo se tra tutte le coppie ce n'è una che sta aspettando all'oracolo
        others_coppie = list(coppie.find({"squadra":players["squadra"], "awaiting":True, "attivo":True, "available":True}))

        if len(others_coppie) == 0:
            #non c'è nemmeno nessuno in fase2, direi che possiamo mandarli all'oracolo a fare qualche cazzata per temporeggiare
            st.success("Andate all'oracolo, dite la parola magica 'epecchè' e ci sarà una sorpresa per voi")
            return
        else:
            #accoppiamo questi con la coppia in fase 2
            altri = {
                "tipo" : "coppia",
                "nomi_coppia" : others_coppie[0]["nomi"],
                "ids":others_coppie[0]["ids"]
            }
            quartetti.update_one(
                players,
                {"$set":{"altri":altri}}
            )
            quartetti.update_one(
                players,
                {"$set": {"available": False}}
            )
            coppie.update_one(
                others_coppie[0],
                {"$set": {"available": False}}
            )
            ids = others_coppie[0]["ids"]
    else:
        #formiamo il quartetto
        altri = {
            "tipo":"quartetto",
            "nomi_coppia" : others_quartetti[0]["nomi"],
            "ids" : others_quartetti[0]["ids"]
        }
        noi = {
            "tipo": "quartetto",
            "nomi_coppia": players["nomi"],
            "ids": players["ids"]
        }
        print(noi)
        #Assegno a entrambi i quartetti le info dell'altro quartetto
        quartetti.update_one(
            players,
            {"$set": {"altri": altri}}
        )
        quartetti.update_one(
            others_quartetti[0],
            {"$set": {"altri": noi}}
        )

        #Setto i quartetti come non disponibili per essere ulteriormente accoppiati
        quartetti.update_one(
            players,
            {"$set": {"available": False}}
        )
        quartetti.update_one(
            others_quartetti[0],
            {"$set": {"available": False}}
        )
        ids = others_quartetti[0]["ids"]

    busta = find_suitable(singoli, ids, selected_stand)

    if busta is not None:
        st.success(f"Consegna la busta numero {int(busta)}")
    else:
        st.error("Non rimane nessuna busta dell'altro quartetto in questo stand")
    return