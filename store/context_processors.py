# store/context_processors.py

import requests

def categorias_api(request):
    try:
        response = requests.get("http://127.0.0.1:8000/api/categorias/")
        if response.status_code == 200:
            return {"categorias_api": response.json().get("results", [])}
    except:
        pass
    return {"categorias_api": []}
