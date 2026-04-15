import hashlib
import json
import time
from pathlib import Path
from typing import Any

from app.config import CACHE_DIR, CACHE_DURATION_SECONDS


def _get_cache_file(key: str) -> Path:
    """
    Restituisce il percorso del file di cache associato a una chiave.

    Input:
        key (str): chiave univoca della richiesta.

    Output:
        Path: percorso del file JSON di cache.

    Casi di errore:
        - Solleva ValueError se la chiave è vuota o non valida.
    """
    if not isinstance(key, str) or not key.strip():
        raise ValueError("La chiave della cache deve essere una stringa non vuota.")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{digest}.json"


def load_from_cache(key: str) -> dict[str, Any] | None:
    """
    Carica un valore dalla cache se presente e ancora valido.

    Input:
        key (str): chiave della richiesta da cercare in cache.

    Output:
        dict | None: dati salvati in cache se validi, altrimenti None.

    Casi di errore:
        - Se il file è corrotto o non leggibile, viene ignorato e restituisce None.
    """
    cache_file = _get_cache_file(key)

    if not cache_file.exists():
        return None

    try:
        with cache_file.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except (OSError, json.JSONDecodeError):
        return None

    timestamp = payload.get("timestamp")
    data = payload.get("data")

    if timestamp is None or data is None:
        return None

    age_seconds = time.time() - timestamp
    if age_seconds >= CACHE_DURATION_SECONDS:
        return None

    return data


def save_to_cache(key: str, data: dict[str, Any]) -> None:
    """
    Salva un valore nella cache su file JSON.

    Input:
        key (str): chiave univoca della richiesta.
        data (dict): dati da memorizzare.

    Output:
        Nessuno.

    Casi di errore:
        - Se il file non può essere scritto, la funzione non interrompe l'app.
    """
    cache_file = _get_cache_file(key)
    payload = {
        "timestamp": time.time(),
        "data": data,
    }

    try:
        with cache_file.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
    except OSError:
        pass