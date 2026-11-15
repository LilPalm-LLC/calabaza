# Calabaza

A mobile-friendly Spanish learning app focused on Mexican Spanish.

## What’s in the app

- **Flashcards:** recall-first cards with original example sentences and simple emoji illustrations.
- **Vocabulary library:** original sample words and phrases organized into A1–A2 Beginner, B1–B2 Intermediate, and C1–C2 Advanced, with practical categories and search.
- **Progress by group:** see remembered, still-learning, and new words for each category.
- **Verb garden:** six subject forms for hablar, comer, vivir, and tener in the present, preterite, and simple future.
- **Word links:** connecting words and question words with examples.

Vocabulary is included in vocabulary.py, so a separate dictionary API is not needed. Supabase is used only for sign-in and saving progress.

## Progress and privacy

When Supabase is configured and you sign in, the app saves only your word ID, status (known or learning), and last review timestamp. It never saves typed answers. Supabase Auth issues an email sign-in code; the app only requests codes for the one email in your local secrets configuration and sets should_create_user to false.

Each progress row belongs to one Supabase Auth user. The SQL migration enables Row Level Security (RLS), grants access only to signed-in users, and applies owner-only read, insert, update, and delete policies. The app sends the signed-in user’s token and publishable key; it never uses a Supabase secret or service-role key.

Without credentials, or if the database is unavailable, practice still works but marks are session-only. A clear message appears; the app will not say that unsaved progress was saved.

## Set up Supabase yourself

No Supabase project or credentials are included in this repository. Create a project only if you choose to use cloud-saved progress.

1. In Supabase, create a project and open SQL Editor. Run supabase/migrations/202611140001_word_progress.sql to create the private progress table and its RLS rules.
2. In Authentication → Users, create/invite only your own user. Keep public sign-ups disabled. Email OTP sign-in is used by the app.
3. Copy .streamlit/secrets.example.toml to .streamlit/secrets.toml. Fill in the project URL, a publishable key, and your approved email. Never paste a secret or service-role key here.
4. Install and start the app:

       python -m venv .venv
       .\.venv\Scripts\Activate.ps1
       pip install -r requirements.txt
       streamlit run app.py

On macOS/Linux, activate with source .venv/bin/activate instead. The real secrets file is ignored by Git.

For a future Streamlit Community Cloud deployment, add the same values in the app’s Secrets settings. Do not commit credentials. Deployment is not included in this change.

## Database size

The app currently has 49 built-in vocabulary entries. The database stores only reviewed-word progress, so one learner’s records should be tiny. Supabase’s current Free plan lists 500 MB of database storage, but free projects can pause after a week of low activity. Check the provider’s current limits before relying on it; usage and plans can change.

## Tests

Run Python unit tests:

       python -m unittest discover -s tests -v

To run the database RLS tests locally, install Docker and the Supabase CLI, then run:

       supabase start
       supabase db reset
       supabase test db
       supabase stop

The RLS test uses two synthetic users and rolls back its fixture data. It checks owner isolation and denies unauthenticated reads/writes. No hosted project is required for that local database test.

## Phone access

Local Streamlit only works on the computer running it unless both devices share a local network. To reach the app away from home and add it to an iPhone home screen, deploy it to an HTTPS host later. iPhone Safari can then use Share → Add to Home Screen. Deployment is intentionally not included.
