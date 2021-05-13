import json
import os

def procitaj(gdje):     # funkcija samo za citanje
    with open(gdje) as f:
        data = json.load(f)
    return data
    
def dodajNaKraj(sto,koji):
    with open(sto, "r+") as file:
        data = json.load(file)
        k = koji.split('///')
        data.update({k[1]:k[0]})
        file.seek(0)
        json.dump(data, file)