# Calabaza

A beginner-friendly Spanish practice app focused on Mexican Spanish, built with Streamlit.

## What’s inside

- **Flashcards:** English prompt first, optional typed recall, answer reveal, example sentence and translation, and “Got it” / “Still learning” session marks.
- **Verb garden:** six person/number forms for *hablar*, *comer*, *vivir*, and *tener* in the present, preterite, and simple future. Uses Mexican *ustedes* for plural “you”; opens with one-at-a-time practice and a full conjugation list.
- **Word links:** searchable connecting words, time/frequency words, and question words with short examples.
- **Phone-friendly layout:** responsive spacing and large buttons.

The illustrations are original emoji cues included in the app; there are no remote image dependencies. Practice marks last only for the current Streamlit session and are not saved between visits.

## Run locally

Python 3.10 or newer is recommended.

On Windows PowerShell:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    streamlit run app.py

On macOS or Linux, activate the environment with `source .venv/bin/activate` before installing and running.

## Open it on your phone

A phone cannot access your computer’s `localhost`. For a quick preview while both devices use the same Wi-Fi, start Streamlit so other devices on your local network can reach it:

    streamlit run app.py --server.address 0.0.0.0

Then open `http://<your-computer-local-IP>:8501` on your phone. Your computer’s firewall may need to allow the connection. This is a temporary local preview, not a public website.

To open the app from anywhere, it needs to be deployed to a reachable HTTPS host. Deployment is not included. After you have a hosted URL:
- **iPhone:** open the URL in Safari, tap Share, then **Add to Home Screen**.
- **Android:** open the URL in Chrome and choose **Add to Home screen** or **Install app** if offered.

This creates a browser-based home-screen shortcut. The exact name, icon, and standalone-app behavior depend on the browser and hosting setup, so check the result on your phone.

## Scope

This starter uses sample content only. It adds no account, secrets, paid services, database, or cross-visit progress storage.
