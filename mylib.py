import json
import os

def procitaj(gdje):     # funkcija samo za citanje
    with open(gdje) as f:
        data = json.load(f)
    return data
    
def dodajNaKraj(sto,koji):
    pass