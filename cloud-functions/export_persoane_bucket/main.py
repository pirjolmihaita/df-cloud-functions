import functions_framework
from google.cloud import firestore, storage
import json
from datetime import datetime

@functions_framework.http
def exporta_persoane(request):
    # Initializează clienții
    db = firestore.Client()
    storage_client = storage.Client()

    # Colectează documentele
    persoane_ref = db.collection("persoane")
    docs = persoane_ref.stream()
    persoane = [doc.to_dict() for doc in docs]

    # Creează un fișier JSON
    json_data = json.dumps(persoane, indent=2)
    filename = f"export_persoane_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Încarcă în bucket
    bucket_name = "persoane-bucket"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(json_data, content_type='application/json')

    return f"✅ Exportat {len(persoane)} persoane în {filename}", 200
