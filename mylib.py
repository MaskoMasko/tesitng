import json
import os

def procitaj(gdje):     # funkcija samo za citanje
    with open(gdje) as f:
        data = json.load(f)
    return data
    
def dodajNaKraj(sto,koji):
    with open(sto, "r+") as file:
        data = json.load(file)
        data.update({sto:"twlve"})
        file.seek(0)
        json.dump(data, file)