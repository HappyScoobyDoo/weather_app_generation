# Weather App (Open-Meteo API)

## Project Overview

This Weather App allows users to check the current weather and 5-day
forecast for any city.\
It uses the Open-Meteo Geocoding API to find location coordinates and
then fetches weather data using the Open-Meteo Weather Forecast API.
The application is built in Python and runs in the terminal. It also
supports displaying weather data for multiple cities side by side.

------------------------------------------------------------------------

## App Features

-   Search input to enter a city name
-   Display of:
    -   Temperature (°C)
    -   Apparent temperature
    -   Wind speed (km/h)
    -   Weather description
-   5-day weather forecast
-   Support for multiple city searches (displayed side by side)
-   Error message if city is not found
-   Error handling for API failures
-   Local caching of weather data (valid for 1 hour)

------------------------------------------------------------------------

## How to Navigate & Run the Code

### Clone this repository

``` bash
git clone https://github.com/HappyScoobyDoo/weather_app_generation.git
```

### Navigate to the project folder

``` bash
cd weather-app-open-meteo
```

### Install dependencies

``` bash
pip install -r requirements.txt
```

### Run the application

``` bash
python run.py
```

### Use the menu

You will see a menu in the terminal:

    1. Current weather
    2. 5-day forecast
    3. Multiple cities (side-by-side)
    4. Exit

------------------------------------------------------------------------

## Project Files

    app/
    ├── api/
    ├── services/
    ├── ui/
    ├── cache.py
    ├── config.py
    ├── models.py
    ├── exceptions.py
    ├── main.py

    run.py
    requirements.txt
    tests/

------------------------------------------------------------------------

## Example Output

    Catania, Italy              Roma, Italy
    Temperatura: 22 °C          Temperatura: 18 °C
    Percepita:   23 °C          Percepita:   18 °C
    Vento:       10 km/h        Vento:       8 km/h
    Aggiornato:  2026-04-15     Aggiornato:  2026-04-15

------------------------------------------------------------------------

## What I Learned

-   How to use APIs in Python
-   Handling HTTP requests and JSON data
-   Structuring a project into multiple modules
-   Error handling and validation
-   Implementing a simple caching system

------------------------------------------------------------------------

## Challenges

-   Managing API responses (geocoding + weather)
-   Handling errors (invalid city, network issues)
-   Keeping the code clean and modular
-   Formatting output in a readable way

------------------------------------------------------------------------

## Future Improvements

-   Add weather icons
-   Improve terminal UI (e.g. using `rich`)
-   Add graphical interface (GUI)
-   Store recent search history
-   Add temperature charts with matplotlib

------------------------------------------------------------------------

## Credits

Weather data provided by Open-Meteo\
https://open-meteo.com/
