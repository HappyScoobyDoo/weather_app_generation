from textwrap import wrap

from app.api.open_meteo import (
    get_current_weather_cached,
    get_five_day_forecast,
    search_city,
)
from app.exceptions import (
    CityNotFoundError,
    InputValidationError,
    InvalidApiResponseError,
)
from app.models import Coordinates, Location


def validate_city_name(city: str) -> str:
    """
    Valida e normalizza il nome della città.

    Input:
        city (str): nome città inserito dall'utente.

    Output:
        str: nome città ripulito dagli spazi laterali.

    Casi di errore:
        - Solleva InputValidationError se il nome è vuoto, non stringa
          o troppo corto per una ricerca sensata.
    """
    if not isinstance(city, str):
        raise InputValidationError("Il nome della città deve essere una stringa.")

    normalized = city.strip()
    if not normalized:
        raise InputValidationError("Il nome della città non può essere vuoto.")

    if len(normalized) < 2:
        raise InputValidationError("Inserisci almeno 2 caratteri per cercare una città.")

    return normalized


def get_location(city: str) -> Location:
    """
    Restituisce la prima località trovata dal servizio di geocoding.

    Input:
        city (str): nome della città da cercare.

    Output:
        Location: località con nome, paese e coordinate.

    Casi di errore:
        - Solleva InputValidationError se l'input non è valido.
        - Solleva CityNotFoundError se la città non viene trovata.
        - Solleva InvalidApiResponseError se mancano coordinate o campi essenziali.
    """
    normalized_city = validate_city_name(city)
    data = search_city(normalized_city)

    results = data.get("results")
    if not results:
        raise CityNotFoundError(f"Città non trovata: {normalized_city}")

    first = results[0]
    latitude = first.get("latitude")
    longitude = first.get("longitude")

    if latitude is None or longitude is None:
        raise InvalidApiResponseError("Coordinate non presenti nella risposta API.")

    name = first.get("name", normalized_city)
    country = first.get("country", "N/D")

    return Location(
        name=name,
        country=country,
        coordinates=Coordinates(latitude=float(latitude), longitude=float(longitude)),
    )


def get_current_weather_by_city(city: str) -> dict:
    """
    Recupera il meteo attuale per una città.

    Input:
        city (str): nome della città.

    Output:
        dict: blocco 'current' della risposta meteo.

    Casi di errore:
        - Solleva InputValidationError se il nome città non è valido.
        - Solleva CityNotFoundError se la città non viene trovata.
        - Solleva InvalidApiResponseError se il blocco 'current' manca.
    """
    location = get_location(city)
    data = get_current_weather_cached(
        latitude=location.coordinates.latitude,
        longitude=location.coordinates.longitude,
    )

    current = data.get("current")
    if not isinstance(current, dict):
        raise InvalidApiResponseError("I dati meteo correnti non sono disponibili.")

    current["_location_name"] = location.name
    current["_country"] = location.country
    return current


def get_five_day_forecast_by_city(city: str) -> dict:
    """
    Recupera la previsione a 5 giorni per una città.

    Input:
        city (str): nome della città.

    Output:
        dict: dizionario con dati località e blocco 'daily'.

    Casi di errore:
        - Solleva InputValidationError se il nome città non è valido.
        - Solleva CityNotFoundError se la città non viene trovata.
        - Solleva InvalidApiResponseError se il blocco 'daily' manca o è incompleto.
    """
    location = get_location(city)
    data = get_five_day_forecast(
        latitude=location.coordinates.latitude,
        longitude=location.coordinates.longitude,
    )

    daily = data.get("daily")
    if not isinstance(daily, dict):
        raise InvalidApiResponseError("La previsione giornaliera non è disponibile.")

    required_fields = [
        "time",
        "weather_code",
        "temperature_2m_min",
        "temperature_2m_max",
    ]
    for field in required_fields:
        if field not in daily:
            raise InvalidApiResponseError(f"Campo mancante nella previsione: {field}")

    return {
        "location_name": location.name,
        "country": location.country,
        "daily": daily,
    }


def weather_code_to_text(code: int) -> str:
    """
    Converte un weather code in una descrizione leggibile.

    Input:
        code (int): codice meteo Open-Meteo.

    Output:
        str: descrizione testuale breve del fenomeno meteo.

    Casi di errore:
        - Se il codice non è noto, restituisce una descrizione generica.
    """
    descriptions = {
        0: "Sereno",
        1: "Prevalentemente sereno",
        2: "Parzialmente nuvoloso",
        3: "Coperto",
        45: "Nebbia",
        48: "Nebbia con brina",
        51: "Pioviggine leggera",
        53: "Pioviggine moderata",
        55: "Pioviggine intensa",
        61: "Pioggia debole",
        63: "Pioggia moderata",
        65: "Pioggia forte",
        71: "Neve debole",
        73: "Neve moderata",
        75: "Neve forte",
        80: "Rovesci deboli",
        81: "Rovesci moderati",
        82: "Rovesci forti",
        95: "Temporale",
    }
    return descriptions.get(code, f"Codice meteo {code}")


def format_current_weather(weather: dict) -> str:
    """
    Converte il meteo attuale in una stringa leggibile.

    Input:
        weather (dict): blocco 'current' con dati meteo e campi località.

    Output:
        str: testo formattato per il terminale.

    Casi di errore:
        - Solleva InputValidationError se il parametro non è un dizionario.
    """
    if not isinstance(weather, dict):
        raise InputValidationError("I dati meteo devono essere un dizionario.")

    city = weather.get("_location_name", "Località")
    country = weather.get("_country", "N/D")
    temperature = weather.get("temperature_2m", "N/D")
    apparent = weather.get("apparent_temperature", "N/D")
    wind = weather.get("wind_speed_10m", "N/D")
    observed_at = weather.get("time", "N/D")

    return (
        f"\n📍 {city}, {country}\n"
        f"🌡️ Temperatura: {temperature} °C\n"
        f"🙂 Percepita:   {apparent} °C\n"
        f"💨 Vento:       {wind} km/h\n"
        f"🕒 Aggiornato:  {observed_at}\n"
        f"\nFonte dati: Open-Meteo\n"
    )


def format_five_day_forecast(forecast: dict) -> str:
    """
    Converte una previsione a 5 giorni in una stringa leggibile.

    Input:
        forecast (dict): dizionario con campi località e blocco 'daily'.

    Output:
        str: testo formattato per il terminale.

    Casi di errore:
        - Solleva InputValidationError se il parametro non è un dizionario valido.
    """
    if not isinstance(forecast, dict) or "daily" not in forecast:
        raise InputValidationError("La previsione fornita non è valida.")

    location_name = forecast.get("location_name", "Località")
    country = forecast.get("country", "N/D")
    daily = forecast["daily"]

    dates = daily["time"]
    codes = daily["weather_code"]
    temp_min = daily["temperature_2m_min"]
    temp_max = daily["temperature_2m_max"]

    lines = [f"\nPrevisione a 5 giorni per {location_name}, {country}:\n"]
    for date, code, t_min, t_max in zip(dates, codes, temp_min, temp_max):
        lines.append(
            f"{date} -> {weather_code_to_text(code)}, min {t_min} °C, max {t_max} °C"
        )

    lines.append("\nFonte dati: Open-Meteo")
    return "\n".join(lines)


def build_city_card(city: str) -> list[str]:
    """
    Costruisce una card testuale con il meteo attuale di una città.

    Input:
        city (str): nome della città.

    Output:
        list[str]: righe testuali della card.

    Casi di errore:
        - In caso di errore, restituisce comunque una card con messaggio esplicativo.
    """
    try:
        weather = get_current_weather_by_city(city)
        return [
            f"{weather.get('_location_name', city)}, {weather.get('_country', 'N/D')}",
            f"Temperatura: {weather.get('temperature_2m', 'N/D')} °C",
            f"Percepita:   {weather.get('apparent_temperature', 'N/D')} °C",
            f"Vento:       {weather.get('wind_speed_10m', 'N/D')} km/h",
            f"Aggiornato:  {weather.get('time', 'N/D')}",
        ]
    except Exception as exc:
        return [
            city,
            "Errore",
            str(exc),
        ]


def format_cards_side_by_side(cards: list[list[str]], width: int = 32, spacing: int = 4) -> str:
    """
    Dispone più card affiancate in colonne a larghezza fissa.

    Input:
        cards (list[list[str]]): elenco di card da visualizzare.
        width (int): larghezza di ogni colonna.
        spacing (int): spazi tra una colonna e l'altra.

    Output:
        str: testo finale pronto da stampare.

    Casi di errore:
        - Solleva InputValidationError se l'elenco delle card è vuoto o non valido.
    """
    if not isinstance(cards, list) or not cards:
        raise InputValidationError("Nessuna card da visualizzare.")

    normalized_cards: list[list[str]] = []
    max_lines = 0

    for card in cards:
        wrapped_lines: list[str] = []
        for line in card:
            wrapped_lines.extend(wrap(str(line), width=width) or [""])
        normalized_cards.append(wrapped_lines)
        max_lines = max(max_lines, len(wrapped_lines))

    for card in normalized_cards:
        while len(card) < max_lines:
            card.append("")

    rows: list[str] = []
    separator = " " * spacing
    for index in range(max_lines):
        row = [card[index].ljust(width) for card in normalized_cards]
        rows.append(separator.join(row))

    rows.append("")
    rows.append("Fonte dati: Open-Meteo")
    return "\n".join(rows)


def get_multiple_cities_weather(cities_input: str) -> str:
    """
    Recupera il meteo attuale per più città e lo restituisce affiancato.

    Input:
        cities_input (str): città separate da virgola.

    Output:
        str: testo formattato con una card per ogni città.

    Casi di errore:
        - Solleva InputValidationError se l'input è vuoto.
        - Le singole città con errore vengono mostrate come card di errore.
    """
    if not isinstance(cities_input, str):
        raise InputValidationError("L'elenco delle città deve essere una stringa.")

    cities = [item.strip() for item in cities_input.split(",") if item.strip()]
    if not cities:
        raise InputValidationError("Inserisci almeno una città separata da virgola.")

    cards = [build_city_card(city) for city in cities]
    return format_cards_side_by_side(cards)