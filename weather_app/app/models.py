from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    """
    Coordinate geografiche di una località.

    Input:
        latitude (float): latitudine della località.
        longitude (float): longitudine della località.

    Output:
        Oggetto Coordinates immutabile.

    Casi di errore:
        - La validazione dei valori viene eseguita prima della creazione.
    """
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Location:
    """
    Informazioni base di una località trovata tramite geocoding.

    Input:
        name (str): nome della località.
        country (str): paese della località.
        coordinates (Coordinates): coordinate geografiche.

    Output:
        Oggetto Location immutabile.

    Casi di errore:
        - La validazione dei dati viene eseguita prima della creazione.
    """
    name: str
    country: str
    coordinates: Coordinates