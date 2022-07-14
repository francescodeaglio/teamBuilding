import streamlit as st

st.write("# Descrizione\n\n"
         "Ciao animatori,\n\nTutto quello che dovete fare è scegliere la sezione 'stand' sulla sinistra e selezionare il vostro stand."
         "Una volta selezionato lo stand troverete tre expander (cliccandoci sopra si aprono).\n\n"
         "### Primo expander\n\n"
         "\n\nIl **primo** è per cambiare lo stand se avete selezionato quello sbagliato."
         "\n\n"
         "### Secondo expander\n\n"
         "Nel **secondo** expander trovate ciò che serve per la _prima fase_ (ovvero quando i giocatori partecipano da soli). E' presente una breve descrizione dello stand (p.s. se a voce vi diciamo qualcosa di diverso, vale quanto detto a voce) e un"
         " box per cercare il giocatore."
         "\n\nOgni stand funziona allo stesso modo: si fa quanto descritto nello stand, se viene superata la prova cercate il cognome di chi ha superato lo stand. "
         "Vi viene fornito un numero, consegnate il foglio con quel numero."
         "\n\n**Esempio:**"
         "\n\nStand **I**, Stefano Terenzi supera la prova")
st.image("media/Pre.png")
st.write("Una volta premuto vi appare una scritta del genere")
st.image("media/Post.png")
st.write("E quindi consegnerete un fogliettino del genere del genere")
st.image("media/Bigliettino.png")
st.write("In questo bigliettino è riportata la materia preferita della persona che Stefano Terenzi sta cercando.")

st.warning("ATTENZIONE: i ragazzi ricevono bigliettini sempre con lo stesso numero (ma con indizi diversi). Se qualcuno lo capisce"
           " e per velocizzare vi dice 'dammi il bigliettino XX' **non fatelo**. Cercate comunque il nome perchè serve a registrare che quell'animato ha completato il vostro stand")

st.write("### Terzo expander")
st.write("Stessa storia ma qua si gioca in quartetti anzichè singoli. GLi stand son diversi, trovate la descrizione per questa fase."
        ""
        "\n\nI bigliettini da consegnare son gli stessi della prima fase. L'unico caso particolare a cui fare attenzione è che, se va di sfiga, non ci sono più bigliettini da consegnare. Questo accade se tutti e quattro i membri del quartetto han già "
        "fatto lo stand nella prima fase. Se succede, vi viene mostrato un messaggio e non consegnate nulla a quel quartetto.")