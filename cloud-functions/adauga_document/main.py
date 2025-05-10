import functions_framework
import random
import math
from google.cloud import firestore
import numpy as np

# Distribuție Laplace
def adauga_zgomot_laplace(valoare_reală, epsilon):
    print(".z")
    b = 1 / epsilon
    zgomot = np.random.laplace(loc=0.0, scale=b)
    return valoare_reală + zgomot

# Funcție HTTP trigger
@functions_framework.http
def adauga_document(request):
    data = request.get_json()

    nume = data.get("nume")
    valoare_reală = data.get("valoare_reală")
    epsilon = data.get("epsilon")

    valoare_cu_zgomot = adauga_zgomot_laplace(valoare_reală, epsilon)

    #  Afișează în log dacă valoarea cu zgomot depășește 100
    if valoare_cu_zgomot > 100:
        print(f"ALERTA: Valoare mare pentru {nume}: {valoare_cu_zgomot}")

    db = firestore.Client()
    db.collection("persoane").add({
        "nume": nume,
        "valoare_reală": valoare_reală,
        "valoare_cu_zgomot": valoare_cu_zgomot,
        "epsilon": epsilon
    })

    return f"Adăugat {nume} cu zgomot: {valoare_cu_zgomot}", 200

