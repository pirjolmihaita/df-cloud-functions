import functions_framework
from flask import jsonify
from google.cloud import firestore

@functions_framework.http
def obtine_documente(request):
    db = firestore.Client()
    rezultate = db.collection("persoane").stream()

    lista = [doc.to_dict() for doc in rezultate]
    return jsonify(lista), 200
