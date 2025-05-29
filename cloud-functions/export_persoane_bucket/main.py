import functions_framework
from google.cloud import firestore, storage
import json
from datetime import datetime
from flask import make_response

@functions_framework.http
def exporta_persoane(request):
    try:
        # Initializeaza clientii Firestore si Storage
        db = firestore.Client()
        storage_client = storage.Client()

        # Citeste documentele din colectia "persoane"
        persoane_ref = db.collection("persoane")
        docs = persoane_ref.stream()
        persoane = []

        for doc in docs:
            data = doc.to_dict()
            # Elimina câmpul venit_real (date sensibile)
            data.pop("venit_real", None)
            persoane.append(data)

        # Verifica daca lista e goala
        if not persoane:
            mesaj = {
                "status": "info",
                "mesaj": "Nu exista persoane In Firestore."
            }
            return make_response(
                json.dumps(mesaj, ensure_ascii=False),
                200,
                {"Content-Type": "application/json"}
            )

        # Creeaza JSON si nume de fisier
        json_data = json.dumps(persoane, indent=2, ensure_ascii=False)
        filename = f"export_persoane_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Incarca In Cloud Storage
        bucket_name = "persoane-bucket"
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(json_data, content_type='application/json')

        mesaj = {
            "status": "success",
            "mesaj": f"Exportat {len(persoane)} persoane In {filename}"
        }
        return make_response(
            json.dumps(mesaj, ensure_ascii=False),
            200,
            {"Content-Type": "application/json"}
        )

    except Exception as e:
        print(f"Eroare: {str(e)}")
        mesaj = {
            "status": "error",
            "mesaj": "A aparut o eroare la exportul persoanelor.",
            "detalii": str(e)
        }
        return make_response(
            json.dumps(mesaj, ensure_ascii=False),
            500,
            {"Content-Type": "application/json"}
        )

