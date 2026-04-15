from app.exceptions import WeatherAppError
from app.services.weather_service import (
    format_current_weather,
    format_five_day_forecast,
    get_current_weather_by_city,
    get_five_day_forecast_by_city,
    get_multiple_cities_weather,
)


def show_menu() -> None:
    """
    Mostra il menu principale dell'app.

    Input:
        Nessuno.

    Output:
        Nessuno.

    Casi di errore:
        - Nessuno.
    """
    print("\n=== Weather App ===")
    print("1. Meteo attuale di una città")
    print("2. Previsione a 5 giorni")
    print("3. Meteo attuale per più città affiancate")
    print("4. Esci")


def handle_current_weather() -> None:
    """
    Gestisce il flusso per il meteo attuale di una singola città.

    Input:
        Nessuno.

    Output:
        Nessuno. Stampa il risultato a schermo.

    Casi di errore:
        - Gli errori applicativi vengono mostrati in modo leggibile.
    """
    city = input("Inserisci una città: ")
    try:
        weather = get_current_weather_by_city(city)
        print(format_current_weather(weather))
    except WeatherAppError as exc:
        print(f"\nErrore: {exc}")


def handle_forecast() -> None:
    """
    Gestisce il flusso per la previsione a 5 giorni.

    Input:
        Nessuno.

    Output:
        Nessuno. Stampa il risultato a schermo.

    Casi di errore:
        - Gli errori applicativi vengono mostrati in modo leggibile.
    """
    city = input("Inserisci una città: ")
    try:
        forecast = get_five_day_forecast_by_city(city)
        print(format_five_day_forecast(forecast))
    except WeatherAppError as exc:
        print(f"\nErrore: {exc}")


def handle_multiple_cities() -> None:
    """
    Gestisce il flusso per più città in formato affiancato.

    Input:
        Nessuno.

    Output:
        Nessuno. Stampa il risultato a schermo.

    Casi di errore:
        - Gli errori applicativi vengono mostrati in modo leggibile.
    """
    cities = input("Inserisci più città separate da virgola: ")
    try:
        print()
        print(get_multiple_cities_weather(cities))
    except WeatherAppError as exc:
        print(f"\nErrore: {exc}")