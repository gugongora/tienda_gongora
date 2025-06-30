# store/context_processors.py

import requests

def categorias_api(request):
    try:
        response = requests.get("54.208.45.218/api/categorias/")
        if response.status_code == 200:
            return {"categorias_api": response.json().get("results", [])}
    except:
        pass
    return {"categorias_api": []}
