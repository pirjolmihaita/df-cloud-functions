import functions_framework
from google.cloud import firestore, storage
import json
from datetime import datetime
from flask import make_response

@functions_framework.http
def exporta_persoane(request):
    try:
        # Inițializează clienții Firestore și Storage
        db = firestore.Client()
        storage_client = storage.Client()

        # Citește documentele din colecția "persoane"
        persoane_ref = db.collection("persoane")
        docs = persoane_ref.stream()
        persoane = []

        for doc in docs:
            data = doc.to_dict()
            # Elimină câmpul venit_real (date sensibile)
            data.pop("venit_real", None)
            persoane.append(data)

        # Verifică dacă lista e goală
        if not persoane:
            mesaj = {
                "status": "info",
                "mesaj": "Nu există persoane în Firestore."
            }
            return make_response(
                json.dumps(mesaj, ensure_ascii=False),
                200,
                {"Content-Type": "application/json"}
            )

        # Creează JSON și nume de fișier
        json_data = json.dumps(persoane, indent=2, ensure_ascii=False)
        filename = f"export_persoane_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Încarcă în Cloud Storage
        bucket_name = "persoane-bucket"
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(json_data, content_type='application/json')

        mesaj = {
            "status": "success",
            "mesaj": f"Exportat {len(persoane)} persoane în {filename}"
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
            "mesaj": "A apărut o eroare la exportul persoanelor.",
            "detalii": str(e)
        }
        return make_response(
            json.dumps(mesaj, ensure_ascii=False),
            500,
            {"Content-Type": "application/json"}
        )

