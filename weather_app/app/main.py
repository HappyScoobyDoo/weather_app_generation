from app.ui.console import (
    handle_current_weather,
    handle_forecast,
    handle_multiple_cities,
    show_menu,
)


def run() -> None:
    """
    Avvia l'applicazione meteo da terminale.

    Input:
        Nessuno.

    Output:
        Nessuno. Gestisce l'interazione con l'utente via terminale.

    Casi di errore:
        - Gli errori delle singole operazioni vengono gestiti nei relativi handler.
    """
    while True:
        show_menu()
        choice = input("Scegli un'opzione: ").strip()

        if choice == "1":
            handle_current_weather()
        elif choice == "2":
            handle_forecast()
        elif choice == "3":
            handle_multiple_cities()
        elif choice == "4":
            print("\nChiusura applicazione.")
            break
        else:
            print("\nScelta non valida. Riprova.")