import functions_framework
import random
import math
from google.cloud import firestore
import numpy as np
from flask import jsonify


# Distribuție Laplace
def adauga_zgomot_laplace(valoare_reală, epsilon):
    print(".")
    b = 1 / epsilon
    zgomot = np.random.laplace(loc=0.0, scale=b)
    return valoare_reală + zgomot

# Funcție HTTP trigger
@functions_framework.http
def adauga_document(request):
    try:
        data = request.get_json()

        nume = data.get("nume")
        valoare_reală = data.get("valoare_reală")
        epsilon = data.get("epsilon")

        if None in (nume, valoare_reală, epsilon):
            return {"error": "Date lipsă în cerere"}, 400

        valoare_cu_zgomot = adauga_zgomot_laplace(valoare_reală, epsilon)

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

    except Exception as e:
        print(f"Eroare: {str(e)}")
        mesaj = {
            "status": "error",
            "mesaj": "A apărut o eroare internă.",
            "detalii": str(e)
        }
        return Response(json.dumps(mesaj, ensure_ascii=False), status=500, mimetype='application/json')


