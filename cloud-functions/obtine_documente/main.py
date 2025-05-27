import functions_framework
from flask import make_response
import json
from google.cloud import firestore

@functions_framework.http
def obtine_documente(request):
    db = firestore.Client()
    rezultate = db.collection("persoane").stream()

    lista = [doc.to_dict() for doc in rezultate]

    if not lista:
        raspuns = {"mesaj": "Nu există nicio persoană în Firestore."}
        return make_response(
            json.dumps(raspuns, ensure_ascii=False),
            200,
            {"Content-Type": "application/json"}
        )

    return make_response(
        json.dumps(lista, ensure_ascii=False),
        200,
        {"Content-Type": "application/json"}
    )

