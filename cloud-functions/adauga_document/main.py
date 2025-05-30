import functions_framework
from google.cloud import firestore
import numpy as np
import json
from flask import Response

# Distributie Laplace
def adauga_zgomot_laplace(valoare_reala, epsilon):
    if epsilon <= 0:
        raise ValueError("Epsilon trebuie sa fie mai mare ca 0")
    b = 1 / epsilon
    zgomot = np.random.laplace(loc=0.0, scale=b)
    return valoare_reala + zgomot

# Funcție HTTP trigger
@functions_framework.http
def adauga_document(request):
    try:
        data = request.get_json()

        id_persoana = data.get("id")
        venit_real = data.get("venit")
        epsilon = data.get("epsilon")

        if None in (id_persoana, venit_real, epsilon):
            return Response(json.dumps({"error": "Date lipsa: id, venit sau epsilon"}, ensure_ascii=False), status=400, mimetype='application/json')

        db = firestore.Client()

        # Verifica daca id-ul deja exista
        doc_ref = db.collection("persoane").document(id_persoana)
        if doc_ref.get().exists:
            return Response(json.dumps({"error": f"Persoana cu ID-ul '{id_persoana}' exista deja."}, ensure_ascii=False), status=409, mimetype='application/json')

        venit_cu_zgomot = adauga_zgomot_laplace(venit_real, epsilon)

        if venit_cu_zgomot > 100:
            print(f"ALERTA: Venit mare pentru ID {id_persoana}: {venit_cu_zgomot}")

        doc_ref.set({
            "venit_real": venit_real,
            "venit_cu_zgomot": venit_cu_zgomot,
            "epsilon": epsilon
        })

        mesaj = {
            "status": "success",
            "mesaj": f"Adaugat ID {id_persoana} cu venit zgomotos: {venit_cu_zgomot:.2f}"
        }
        return Response(json.dumps(mesaj, ensure_ascii=False), status=200, mimetype='application/json')

    except Exception as e:
        print(f"Eroare: {str(e)}")
        mesaj = {
            "status": "error",
            "mesaj": "A aparut o eroare interna.",
            "detalii": str(e)
        }
        return Response(json.dumps(mesaj, ensure_ascii=False), status=500, mimetype='application/json')



