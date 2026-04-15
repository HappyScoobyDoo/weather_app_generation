import requests


def fetch_weather(latitude, longitude):
    """
    Recupera i dati meteo correnti da Open-Meteo usando latitudine e longitudine.

    Input:
        latitude (float): latitudine della località.
        longitude (float): longitudine della località.

    Output:
        dict: risposta JSON dell'API Open-Meteo convertita in dizionario Python.

    Casi di errore:
        - Solleva un'eccezione se la richiesta HTTP fallisce.
        - Solleva un'eccezione se l'API restituisce un codice di stato non valido.
        - Può fallire se latitude o longitude non sono numeri validi.
        - Può fallire se la risposta dell'API non è nel formato atteso.
    """
    
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current_weather=true"
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Errore nella richiesta API meteo")

    return response.json()