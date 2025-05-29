# Scraping Search Project

Questo progetto raccoglie e visualizza i prodotti in offerta su Amazon utilizzando Flask per creare una dashboard di ricerca.

## Setup

1. Clona questo repository
2. Installa le dipendenze:

   ```bash
   pip install -r requirements.txt
   ```

3. Esegui l'app Flask:

   ```bash
   python src/main.py
   ```

4. Accedi all'app su `http://127.0.0.1:5000`.

## Deployment su Render

1. Collega il progetto a **Render**.
2. Imposta il comando di avvio su `gunicorn src.main:app`.
3. Fai il deploy del progetto su Render.
