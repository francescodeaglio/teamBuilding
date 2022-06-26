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
        "L": "Youtuber preferito",
    }
    return stands

def get_labels_stands():
    stands = get_stands()
    labels = [key + " - " + stands[key] for key in stands]
    return labels

def get_descrizione_individui():
    descrizione = {
        "A": "Fai questo...",
        "B": "Fai quello",
        "C": "Dai su",
        "D": "Qualcosa su Sport o hobby",
        "E": "Uno stand about Cosa vuoi fare da grande",
        "F": "Riproduci questo o quest'altro",
        "G": "Dai",
        "H": "Peffavore",
        "I": "TODO",
        "L": "Youtuber preferito Tommo",
    }
    return descrizione

def get_descrizione_quartetti():
    descrizione = {
        "A": "Fai questo...",
        "B": "Fai quello",
        "C": "Dai su",
        "D": "Qualcosa su Sport o hobby",
        "E": "Uno stand about Cosa vuoi fare da grande",
        "F": "Riproduci questo o quest'altro",
        "G": "Dai",
        "H": "Peffavore",
        "I": "TODO",
        "L": "Youtuber preferito Tommo",
    }
    return descrizione