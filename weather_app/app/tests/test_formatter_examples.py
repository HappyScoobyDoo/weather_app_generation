from app.services.weather_service import format_cards_side_by_side, weather_code_to_text


def test_weather_code_to_text_known_value():
    assert weather_code_to_text(0) == "Sereno"


def test_format_cards_side_by_side_returns_text():
    cards = [
        ["Catania, Italy", "Temperatura: 20 °C"],
        ["Roma, Italy", "Temperatura: 18 °C"],
    ]
    result = format_cards_side_by_side(cards)
    assert "Catania, Italy" in result
    assert "Roma, Italy" in result