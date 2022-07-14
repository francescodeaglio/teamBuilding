def get_stands():
    stands = {
        "A": "Colore preferito",
        "B": "Età",
        "C": "Cibo preferito",
        "D": "Sport o hobby",
        "E": "Cosa vuoi fare da grande",
        "F": "Serie TV preferita",
        "G": "Cantante/Gruppo preferito",
        "H": "Gioco preferito al campo",
        "I": "Materia preferita a scuola",
        "J": "Youtuber preferito",
    }
    return stands

def get_labels_stands():
    stands = get_stands()
    labels = [key + " - " + stands[key] for key in stands]
    return labels

def get_descrizione_individui():
    descrizione = {
        "A": "Twister: si gioca a gruppi di 4 persone. Il primo che cade perde e rimane li. Gli altri 3 ricevono il bigliettino. A questo punto il gioco ricomincia con 3 nuovi partecipanti + il perdente della manche precedente. ",
        "B": "Equazione: breve equazione (4 addendi) da risolvere. Lo stand da il bigliettino e l’animato riceve il foglietto se da la risposta corretta (con una certa tolleranza)",
        "C": "Riconosci le spezie dal profumo: comprare 5/6 spezie(o altra roba distinguibile dall’odore tipo caffè o Seba) diverse e produrre altrettanti vasetti con le spezie mischiate. I partecipanti ricevono un vasetto e devono indovinare le spezie presenti all’interno solo dal profumo. Grading scale: 3-4-5-6: bigliettino,1-2: nulla,	0: tampone COVID seduta stante",
        "D": """Corse suddivise in varie fasi\n
|--------------------|----------|-----------------|--------------------------------|\n\ncanestro
pallina in bocca|mattoni|corsa sacchi| palleggio pallina/racchetta pingpong
""",
        "E": """Cosa fanno i grandi: domande del tipo “dimmi il nome di un animatore che studia ingegneria”, “Dove si trova il bar di carmela”, “quali animatori vivono all’estero”...
Ognuno riceve 3 domande e deve rispondere correttamente (⅔ passing).
""",
        "F": """Seriebanda: prepare un video da un minuto con tot spezzoni da 10 serie diverse (the office, casa di carta ma anche qualcosa per i più piccoli (peppa pig o magari qualcosa di più nuovo che grazie al cielo non conosco)). Prova in salone, vengono fatte entrare 4 persone per volta. Le persone collaborano e l’obiettivo è azzeccare 8 serie. Se azzeccano, tutti e 4 prendono il bigliettino. Altrimenti byebye""",
        "G": "Somma le canzoni: Vengono creati due medley dalle canzoni di sotto che sono appositamente scelte per essere piene di numeri. Partecipano 4 persone per volta e l’obiettivo è sommare tutti i numeri detti. Chi si avvicina di meno non riceve nulla, tutti gli altri ottengono un bigliettino. (magari dare calcolatrice ai più piccoli)",
        "H": """Lo stand si fa a gruppetti per velocizzare (4 persone). L’animatore indossa una maschera horror e maneggia uno spruzzino tipo vetril pieno d’acqua. L’animatore inizia raccontando una storia idiota tipo adventure in cui si introducono le quattro prove effettive. Una volta finita la storia, viene assegnata una prova diversa a ogni partecipante
-	ok il prezzo è giusto
-	indovinello/indizio (caccia al tesoro)
-	2x sfida coccodrilli/galli cedroni ecc
""",
        "I": """Geografia: mappa dell’italia/mondo tipo Ciao darwin, domanda tipo “dov’è il monte bianco?”, indicami il nepal…
Storia: timeline stampata, ci sono dei post it con degli eventi. I giocatori devono posizionare gli eventi sulla timeline correttamente.
Italiano: coniugare un verbo (ex trapassato prossimo di volare)
""",
        "L": "Bottleflip challenge: as it is. Quando riuscita, viene consegnato il bigliettino.",
    }
    return descrizione

def get_descrizione_quartetti():
    descrizione = {
        "A": "Palloncino a quattro mani: ognuno dei 4 partecipanti impugna un lenzuolo da una delle 4 estremità. Sul lenzuolo viene posto un palloncino pieno d’acqua e l’obiettivo è fare canestro in un secchio. Più tentativi available but dopo che han distrutto un tot di palloncini se ne vanno a calci in culo.",
        "B": "Canalina mobile: cartoncini di carta piegati a U / sezione di tubo per far scorrere una pallina all’interno. L’obiettivo è percorrere X metri. GIoco 2 nel video",
        "C": "Torre di Aimasso: Torre di Hanoi",
        "D": "Spaghetti Challenge - Sciacchia Edition: i componenti devono costruire una torre almeno alta X usando spaghetti, scotch ma non la voce.",
        "E": "Colloquio: dobbiamo assumere un nuovo vicepresidente dell’associazione. Quello attuale ha come skills: francese, educazione fisica e 1 occhio. Dimostrate che sapete fare meglio di lui per venire assunti. Fare domande-meme AMMP tipo come girare la polenta, come tuffare i grustel nell’acqua rossa, come aromatizzare i risotti, scegli la punta di trapano adatta per invadere il box dei vicini, spiega come spaccare le piastrelle, ",
        "F": "Mi chiamo massimo decimo merìdio: prova di recitazione. Copione a 4 voci, riprodurlo convincentevolmente.",
        "G": "Karaoke: cantate una canzone, dai!",
        "H": "Corse: c’è un pool di materiali e devono creare un gioco con quattro corse usando gli oggetti a disposizione",
        "I": """Simile alla fase precedente
Arte: idem con la mappa, bisogna collocare sulla mappa il monumento/il paese dell’artista/dove è conservato
Scienze: scala delle potenze di 10, bisogna collocare degli oggetti (atomo, distanza terra luna, diametro dei coglioni di buda granny…)
""",
        "L": "Youtuberbanda: prepare un video da un minuto con tot spezzoni da 10 youtubers diverse (cicciogamer, tommo, Me contro Te, Lvis, cosa mangiamo oggi, sio, ). Devono indovinare sufficientemente tanti.",
    }
    return descrizione