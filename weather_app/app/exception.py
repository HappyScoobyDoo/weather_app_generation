class WeatherAppError(Exception):
    """Eccezione base dell'app meteo."""


class InputValidationError(WeatherAppError):
    """Errore di validazione dell'input utente."""


class CityNotFoundError(WeatherAppError):
    """La città richiesta non è stata trovata."""


class ApiRequestError(WeatherAppError):
    """Errore durante la chiamata a un servizio esterno."""


class InvalidApiResponseError(WeatherAppError):
    """La risposta API è assente, incompleta o malformata."""