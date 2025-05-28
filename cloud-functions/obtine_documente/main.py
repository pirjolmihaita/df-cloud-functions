import functions_framework
from flask import make_response
import json
from google.cloud import firestore

@functions_framework.http
def obtine_documente(request):
    try:
        db = firestore.Client()
        rezultate = db.collection("persoane").stream()
        lista = [doc.to_dict() for doc in rezultate]

        if not lista:
            raspuns = {"mesaj": "Nu există nicio persoană în Firestore."}
            return Response(json.dumps(raspuns, ensure_ascii=False), status=200, mimetype='application/json')

        return Response(json.dumps(lista, ensure_ascii=False), status=200, mimetype='application/json')

    except Exception as e:
        print(f"Eroare: {str(e)}")
        mesaj = {
            "status": "error",
            "mesaj": "A apărut o eroare internă.",
            "detalii": str(e)
        }
        return Response(json.dumps(mesaj, ensure_ascii=False), status=500, mimetype='application/json')
