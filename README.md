# Calabaza

A mobile-friendly Spanish learning app focused on Mexican Spanish.

## What’s in the app

- **Flashcards:** recall-first cards with original example sentences and simple emoji illustrations.
- **Vocabulary library:** 500 new original daily-use words and phrases in 20 batches of 25, plus the original starter set. Browse by level, topic, batch, or search Spanish and English.
- **Progress by group:** see remembered, still-learning, and new words for each category.
- **Verb garden:** 100 distinct useful verbs, five per batch, with six Mexican Spanish subject forms in the present, preterite, and simple future. Forms stay hidden until revealed.
- **Sentence practice:** 100 original everyday sentence cards, five per batch, with English-first prompts, Spanish reveal, and saved review status.\n- **Word links:** connecting and question words with examples.

Vocabulary is included in vocabulary.py, so a separate dictionary API is not needed. Supabase is used only for sign-in and saving progress.

## Progress and privacy

When Supabase is configured and you sign in, the app saves only your word ID, status (known or learning), and last review timestamp. It never saves typed answers. Supabase Auth issues an email sign-in code; the app only requests codes for the one email in your local secrets configuration and sets should_create_user to false.

Each progress row belongs to one Supabase Auth user. The SQL migration enables Row Level Security (RLS), grants access only to signed-in users, and applies owner-only read, insert, update, and delete policies. The app sends the signed-in user’s token and publishable key; it never uses a Supabase secret or service-role key.

Without credentials, or if the database is unavailable, practice still works but marks are session-only. A clear message appears; the app will not say that unsaved progress was saved.

## Connect your existing Supabase project (one account)

Your Supabase project already includes the Postgres database. Calabaza needs one extra table called `word_progress`; the existing `projects` and `tasks` tables are unrelated and can stay as they are. Vocabulary is bundled in the app, so the database stores learner progress only.

1. In Supabase, open **SQL Editor → New query**. Open [`supabase/migrations/202611140001_word_progress.sql`](https://github.com/LilPalm-LLC/calabaza/blob/feat/spanish-learning-app/supabase/migrations/202611140001_word_progress.sql), copy its full contents, paste into the query, and click **Run**. This creates the progress table and owner-only RLS rules. It does not change or delete your other tables.
2. In **Authentication → Users**, add your email as a user. Keep public sign-ups disabled. The app only sends a one-time sign-in code to the one email in its configuration, and it will not create accounts.
3. Get your project URL and **publishable** key from the Supabase project’s API settings. Do not use or share a secret/service-role key.
4. For local use, copy `.streamlit/secrets.example.toml` to `.streamlit/secrets.toml`, then replace the placeholders with your URL, publishable key, and the same email you added in Auth:

       [supabase]
       url = "https://YOUR_PROJECT_REF.supabase.co"
       publishable_key = "sb_publishable_YOUR_KEY"
       allowed_email = "you@example.com"

   The real secrets file is ignored by Git. For Streamlit hosting, put these same values in the app’s Secrets settings instead of committing them.
5. Install and start the app:

       python -m venv .venv
       .\.venv\Scripts\Activate.ps1
       pip install -r requirements.txt
       streamlit run app.py

   On macOS/Linux, activate with `source .venv/bin/activate`.

If Supabase is not configured, or the table cannot be reached, the app clearly says marks are session-only. Do not treat progress as saved until you can sign in, mark a card, reopen the app, and see the mark still there.
## Database size

The app bundles 500 new word and phrase entries, 100 additional verb entries, 100 sentence cards, and the original starter set. These are app content, not database rows. The database stores only reviewed-word progress, so one learner’s records should be tiny. Supabase’s current Free plan lists 500 MB of database storage, but free projects can pause after a week of low activity. Check the provider’s current limits before relying on it; usage and plans can change.

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
