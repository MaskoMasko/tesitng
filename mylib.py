import json
import os

def procitaj(gdje):     # funkcija samo za citanje
    with open(gdje) as f:
        data = json.load(f)
    return data
    
def dodajNaKraj(sto,koji):
    with open(sto, "r+") as file:
        data = json.load(file)
        zadnjiBroj = list(data.keys())[-1]
        zadnjiBroj = str(int(zadnjiBroj) + 1)
        k = koji.split('///')
        jeje = {zadnjiBroj:{k[1]:k[0]}}
        data.update(jeje)
        file.seek(0)
        json.dump(data, file)