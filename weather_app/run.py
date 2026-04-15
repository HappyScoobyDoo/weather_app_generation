from app.main import run

if __name__ == "__main__":
   def run():
    """
    Avvia l'applicazione meteo da terminale.

    Input:
        Nessuno.

    Output:
        Nessun valore di ritorno.
        La funzione legge il nome di una città da input utente e stampa
        a schermo le informazioni meteo oppure un messaggio di errore.

    Casi di errore:
        - Se l'utente inserisce una città non valida o non trovata,
          viene mostrato un messaggio di errore.
        - Se si verifica un problema durante il recupero dei dati meteo,
          l'errore viene intercettato e stampato a schermo.
    """