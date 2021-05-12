import json
import os

def procitaj(gdje):     # funkcija samo za citanje
    with open(gdje) as f:
        data = json.load(f)
    return data
    
def dodajNaKraj(sto,koji):
    with open(koji, "r+") as file:
        data = json.load(file)
        data.update(sto)
        file.seek(0)
        json.dump(data, file)