import html
import os
import random

import streamlit as st

from verbs import VERBS, SUBJECTS, TENSES, conjugate
from sentences import SENTENCES

from storage import (
    ProgressStore,
    create_user_client,
    load_config,
    request_email_code,
    verified_user_id,
    verify_email_code,
)
from vocabulary import (
    CATEGORIES,
    LEVELS,
    VOCABULARY,
    BATCHES,
    BATCH_TITLES,
    filter_words,
    summarize_progress,
)

st.set_page_config(
    page_title="Calabaza | Spanish practice",
    page_icon="🎃",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
:root { --ink:#29372d; --muted:#68766b; --cream:#fbf8f0; --green:#315c45; --leaf:#e8f0df; --peach:#fff0df; }
html, body, [class*="css"] { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
.stApp { background:var(--cream); color:var(--ink); }
[data-testid="stHeader"] { background:rgba(251,248,240,.92); }
.block-container { width:100%; max-width:700px; padding:calc(env(safe-area-inset-top,0px) + 1rem) 1rem calc(env(safe-area-inset-bottom,0px) + 4rem); }
h1,h2,h3 { color:var(--ink); } h1 { font-family:Georgia,serif; letter-spacing:-.045em; line-height:1.08; }
.hero { background:linear-gradient(140deg,#fffdf8 5%,#f4eddd 100%); border:1px solid #eee7d8; border-radius:24px; padding:1.1rem 1.2rem .8rem; margin:.25rem 0 1rem; box-shadow:0 8px 24px #343d2d0a; }
.hero h1 { margin:.35rem 0; font-size:clamp(2rem,8vw,3rem); }
.hero p { color:var(--muted); font-size:1rem; margin:.25rem 0 .35rem; }
.eyebrow { color:var(--green); font-weight:750; letter-spacing:.11em; font-size:.72rem; text-transform:uppercase; }
.card { background:#fffefa; border:1px solid #ece8dc; border-radius:22px; padding:1.1rem; margin:.6rem 0 .9rem; box-shadow:0 8px 25px #333f310b; }
.visual { background:radial-gradient(circle at 50% 45%,#fff9e9,#f3ebd8 70%); border:1px solid #f0e7d6; height:138px; border-radius:18px; display:flex; align-items:center; justify-content:center; font-size:4.5rem; margin-bottom:1rem; }
.prompt { color:var(--muted); font-size:.77rem; font-weight:750; letter-spacing:.1em; text-transform:uppercase; }
.answer { font-family:Georgia,serif; font-size:1.9rem; line-height:1.18; font-weight:700; color:var(--green); margin:.2rem 0; overflow-wrap:anywhere; }
.translation { color:var(--muted); font-style:italic; line-height:1.5; }
.soft-note { background:var(--leaf); border:1px solid #dce8d4; border-radius:15px; padding:.8rem .95rem; margin-top:.75rem; line-height:1.5; }
.word-chip { display:inline-block; background:var(--leaf); color:var(--green); padding:.28rem .7rem; border-radius:99px; font-weight:750; }
.word-card { background:#fffefa; border:1px solid #ece8dc; border-radius:18px; padding:.9rem 1rem; margin:.55rem 0; }
.status-pill { background:#fff0df; color:#80511f; border-radius:99px; padding:.2rem .55rem; font-size:.78rem; font-weight:700; }
[data-testid="stTabs"] [role="tablist"] { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:.28rem; background:#fffefa; border:1px solid #eee8dc; border-radius:18px; padding:.32rem; }
[data-testid="stTabs"] button[role="tab"] { justify-content:center; min-height:48px; border-radius:13px; font-size:.86rem; font-weight:750; white-space:nowrap; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { background:var(--green); color:white; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"],[data-testid="stTabs"] [data-baseweb="tab-border"] { display:none; }
[data-testid="stMetric"] { background:#fffefa; border:1px solid #ece8dc; border-radius:16px; padding:.7rem; }
[data-testid="stTextInputRootElement"] input { min-height:48px; border-radius:14px; }
div.stButton > button,div.stFormSubmitButton > button { min-height:48px; border-radius:15px; font-weight:750; border-color:#dce4d8; }
div.stButton > button[kind="primary"],div.stFormSubmitButton > button[kind="primary"] { background:var(--green); border-color:var(--green); }
.stSelectbox [data-baseweb="select"] > div { min-height:48px; border-radius:14px; }
.footnote { color:var(--muted); font-size:.84rem; text-align:center; }
@media(max-width:560px) {
 .block-container { padding-left:.8rem; padding-right:.8rem; }
 .hero { border-radius:21px; padding:1rem; }
 [data-testid="stTabs"] [role="tablist"] { gap:.18rem; padding:.25rem; }
 [data-testid="stTabs"] button[role="tab"] { min-height:48px; font-size:.77rem; padding:.2rem .1rem; }
 .visual { height:122px; font-size:4rem; }
 .card { padding:.95rem; border-radius:19px; }
 .answer { font-size:1.75rem; }
 div.stButton > button { font-size:.9rem; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
 <div class="eyebrow">A little Spanish, every day</div>
 <h1>¡Hola! Soy Calabaza 🎃</h1>
 <p>Words for real life, organized by level and topic.</p>
</div>
""", unsafe_allow_html=True)

try:
    secret_values = st.secrets
except Exception:
    secret_values = {}

config_error = None
try:
    config = load_config(secret_values, os.environ)
except ValueError as error:
    config = None
    config_error = str(error)

client = None
user_id = None
progress = {}
progress_store = None
database_ready = False

if config:
    saved_session = st.session_state.get("supabase_session")
    if saved_session:
        try:
            client = create_user_client(config, saved_session)
            user_id = verified_user_id(client)
            progress_store = ProgressStore(client, user_id)
            progress = progress_store.load()
            database_ready = True
        except Exception:
            st.session_state.pop("supabase_session", None)
            st.session_state.pop("pending_email", None)
            st.session_state.session_progress = {}
            st.warning("We couldn’t restore saved progress. Sign in again or check the database setup.")
            user_id = None
            progress_store = None
            client = None

    if client is None:
        try:
            client = create_user_client(config)
        except Exception:
            client = None

if "session_progress" not in st.session_state:
    st.session_state.session_progress = {}

session_only_progress = st.session_state.session_progress
if not database_ready:
    progress = session_only_progress

if not config:
    st.info("Saved progress isn’t connected yet. You can practice now, but marks will last only in this open session.")
    if config_error:
        st.caption(config_error)
elif user_id:
    auth_left, auth_right = st.columns([3, 1])
    with auth_left:
        st.success("Signed in · progress saves to your private account")
    with auth_right:
        if st.button("Sign out", key="sign_out"):
            try:
                if client:
                    client.auth.sign_out()
            except Exception:
                pass
            st.session_state.pop("supabase_session", None)
            st.session_state.pop("pending_email", None)
            st.session_state.session_progress = {}
            st.rerun()
else:
    with st.expander("Sign in to save your progress", expanded=True):
        if client is None:
            st.error("The database connection could not be created. Check the setup in README.md.")
        else:
            with st.form("request_code_form"):
                email_input = st.text_input("Your approved email")
                send_code = st.form_submit_button("Email me a sign-in code", type="primary", use_container_width=True)
            if send_code:
                if email_input.strip().casefold() != config.allowed_email:
                    st.error("This app is configured for one approved email address.")
                else:
                    try:
                        request_email_code(client, email_input)
                        st.session_state.pending_email = email_input.strip()
                        st.success("Check your email for a one-time code.")
                    except Exception:
                        st.error("We couldn’t send a code. Check the Supabase Auth setup and try again.")
            pending_email = st.session_state.get("pending_email")
            if pending_email:
                with st.form("verify_code_form"):
                    otp = st.text_input("One-time code", max_chars=8, autocomplete="one-time-code")
                    verify = st.form_submit_button("Verify and continue", type="primary", use_container_width=True)
                if verify:
                    try:
                        fresh_client = create_user_client(config)
                        tokens = verify_email_code(fresh_client, pending_email, otp)
                        st.session_state.supabase_session = tokens
                        st.session_state.pop("pending_email", None)
                        st.rerun()
                    except Exception:
                        st.error("That code didn’t work or has expired. Request a new code and try again.")

if config and user_id and not database_ready:
    st.warning("Saved progress couldn’t be loaded. Your next marks will be session-only until the database setup is fixed.")
elif config and not user_id:
    st.caption("Only the approved email can sign in. New account creation is disabled.")

def mark_progress(word_id, status):
    """Save only status and review time; typed answers never reach storage."""
    if database_ready and progress_store:
        try:
            row = progress_store.save(word_id, status)
            progress[word_id] = row
            return True
        except Exception:
            st.error("This mark wasn’t saved. Check your connection and database setup.")
            return False
    row = {"word_id": word_id, "status": status, "last_reviewed_at": None}
    session_only_progress[word_id] = row
    progress[word_id] = row
    return True


def progress_label(word_id):
    row = progress.get(word_id)
    if not row:
        return "New"
    return "Got it" if row.get("status") == "known" else "Still learning"


flashcards_tab, library_tab, verbs_tab, words_tab, sentences_tab = st.tabs(
    ["🗂️ Cards", "🌼 Library", "🌱 Verbs", "🔗 Words", "💬 Sentences"]
)

with flashcards_tab:
    st.markdown('<div class="eyebrow">Recall first, reveal second</div>', unsafe_allow_html=True)
    flashcards = [word for word in VOCABULARY if word["category"] != "Verbs"]
    if "card_index" not in st.session_state:
        st.session_state.card_index = 0
    if "card_revealed" not in st.session_state:
        st.session_state.card_revealed = False
    card_index = st.session_state.card_index % len(flashcards)
    card = flashcards[card_index]
    st.markdown(
        f'<div class="card"><div class="visual" role="img" aria-label="Illustration for {html.escape(card["english"])}">{card["emoji"]}</div><div class="prompt">{html.escape(card["level"])}</div><h2>{html.escape(card["english"])}</h2></div>',
        unsafe_allow_html=True,
    )
    st.text_input("Try to remember the Spanish", key=f"answer_{card['id']}", placeholder="Type it, or think of it")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Reveal answer", type="primary", use_container_width=True, key="reveal_card"):
            st.session_state.card_revealed = True
    with col_b:
        st.caption(f"Card {card_index + 1} of {len(flashcards)}")
    if st.session_state.card_revealed:
        st.markdown(
            f'<div class="card"><span class="word-chip">{html.escape(card["spanish"])}</span><p class="translation"><i>{html.escape(card["example"])}</i><br>{html.escape(card["example_translation"])}</p></div>',
            unsafe_allow_html=True,
        )
        st.caption(f"Your status: {progress_label(card['id'])}")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Still learning", use_container_width=True, key="card_learning"):
                if mark_progress(card["id"], "learning"):
                    st.session_state.card_index = (card_index + 1) % len(flashcards)
                    st.session_state.card_revealed = False
                    st.rerun()
        with col_b:
            if st.button("Got it ✓", type="primary", use_container_width=True, key="card_known"):
                if mark_progress(card["id"], "known"):
                    st.session_state.card_index = (card_index + 1) % len(flashcards)
                    st.session_state.card_revealed = False
                    st.rerun()
    summary = summarize_progress(flashcards, progress)
    metric_a, metric_b = st.columns(2)
    metric_a.metric("Got it", summary["known"])
    metric_b.metric("Still learning", summary["learning"])
    st.caption("Typed answers are used only for your recall attempt; they are never saved.")

with library_tab:
    st.markdown('<div class="eyebrow">Your word garden</div>', unsafe_allow_html=True)
    level = st.selectbox("Learning level", ["All levels", *LEVELS], key="library_level")
    selected_batch = st.selectbox("Study batch", ["All batches", *BATCH_TITLES], key="library_batch")
    batch_number = "All batches" if selected_batch == "All batches" else selected_batch
    all_for_level = filter_words(level=level, batch=batch_number)
    st.markdown("#### Progress by category")
    for category_name in CATEGORIES:
        group = [word for word in all_for_level if word["category"] == category_name]
        if not group:
            continue
        group_summary = summarize_progress(group, progress)
        with st.expander(f"{category_name} · {group_summary['known']}/{group_summary['total']} remembered"):
            st.progress(group_summary["known"] / group_summary["total"])
            st.caption(f"{group_summary['learning']} learning · {group_summary['new']} new")

    category = st.selectbox("Category", ["All categories", *CATEGORIES], key="library_category")
    query = st.text_input("Search Spanish or English", placeholder="Try café, often, where…", key="library_search")
    words = filter_words(level=level, category=category, query=query, batch=batch_number)
    current_summary = summarize_progress(words, progress)
    st.caption(f"{current_summary['total']} words and phrases")
    st.progress(current_summary["known"] / current_summary["total"] if current_summary["total"] else 0)
    if not words:
        st.info("No matches yet. Try another search or category.")
    for word in words:
        with st.container(border=True):
            top_left, top_right = st.columns([3, 1])
            with top_left:
                st.markdown(f'<span class="word-chip">{word["emoji"]} {html.escape(word["spanish"])}</span> &nbsp; <b>{html.escape(word["english"])}</b>', unsafe_allow_html=True)
                st.caption(f'{word["level"]} · {word["category"]}')
                if word.get("example"):
                    st.markdown(f'*{html.escape(word["example"])}*  \n{html.escape(word["example_translation"])}')
                if word.get("batch_title"):
                    st.caption("Batch " + str(word["batch_number"]).zfill(2) + " · " + word["batch_title"])
            with top_right:
                st.markdown(f'<span class="status-pill">{progress_label(word["id"])}</span>', unsafe_allow_html=True)
                if st.button("Got it", key=f"known_{word['id']}", use_container_width=True):
                    if mark_progress(word["id"], "known"):
                        st.rerun()
                if st.button("Review", key=f"learning_{word['id']}", use_container_width=True):
                    if mark_progress(word["id"], "learning"):
                        st.rerun()

with verbs_tab:
    st.markdown('<div class="eyebrow">100 useful verbs · six subject forms</div>', unsafe_allow_html=True)
    selected_batch = st.selectbox("Verb batch", ["All batches", *BATCH_TITLES], key="verb_batch")
    batch_no = None if selected_batch == "All batches" else int(selected_batch.split()[1])
    verbs_for_batch = [verb for verb in VERBS if batch_no is None or verb["batch_number"] == batch_no]
    verb_id = st.selectbox("Choose a verb", [v["id"] for v in verbs_for_batch], format_func=lambda key: next(v["infinitive"] + " — " + v["english"] for v in verbs_for_batch if v["id"] == key), key="verb_choice")
    verb = next(v for v in verbs_for_batch if v["id"] == verb_id)
    tense = st.selectbox("Choose a tense", list(TENSES), key="verb_tense")
    st.markdown('<div class="soft-note"><b>Present</b>: now or usual actions. <b>Preterite</b>: completed past actions. <b>Simple future</b>: what will happen. Mexican Spanish uses <i>ustedes</i> for plural “you”; everyday Mexican Spanish does not use <i>vosotros</i>.</div>', unsafe_allow_html=True)
    key = (verb_id, tense)
    if st.session_state.get("verb_prompt") != key:
        st.session_state.verb_prompt = key
        st.session_state.verb_revealed = False
    st.markdown(f'<div class="card"><div class="prompt">{tense} · {verb["english"]}</div><div class="answer">{html.escape(verb["infinitive"])}</div></div>', unsafe_allow_html=True)
    if st.button("Reveal six forms", type="primary", use_container_width=True, key="reveal_all_verb"):
        st.session_state.verb_revealed = True
    forms = conjugate(verb["infinitive"], tense)
    if st.session_state.get("verb_revealed"):
        for index, (subject, gloss) in enumerate(SUBJECTS):
            st.markdown(f"**{subject}** · {gloss} — **{forms[index]}**")
    st.caption(f'Batch {verb["batch_number"]:02d} · {verb["level"]}')
    st.info("Each verb is grouped in the same 20 study batches as the vocabulary. Sentence practice supplies short real-life examples for these topics.")

with words_tab:
    st.markdown('<div class="eyebrow">Small words, big connections</div>', unsafe_allow_html=True)
    kind = st.selectbox("Word group", ["Connecting words", "Question words"], key="word_group")
    query = st.text_input("Search this group", placeholder="Try y, always, why, where…", key="word_search")
    entries = filter_words(category=kind, query=query)
    if not entries:
        st.info("No matches yet. Try another word or meaning.")
    for word in entries:
        st.markdown(f'<div class="word-card"><span class="word-chip">{html.escape(word["spanish"])}</span> &nbsp; <b>{html.escape(word["english"])}</b><br><i>{html.escape(word["example"])}</i><br>{html.escape(word["example_translation"])}</div>', unsafe_allow_html=True)
        st.caption(f'{word["level"]} · {progress_label(word["id"])}')

with sentences_tab:
    st.markdown('<div class="eyebrow">100 everyday sentences · five per batch</div>', unsafe_allow_html=True)
    sentence_batch = st.selectbox("Sentence batch", BATCH_TITLES, key="sentence_batch")
    sentence_batch_no = int(sentence_batch.split()[1])
    sentences = [s for s in SENTENCES if s["batch_number"] == sentence_batch_no]
    if "sentence_index" not in st.session_state:
        st.session_state.sentence_index = 0
    sentence_index = st.session_state.sentence_index % len(sentences)
    sentence = sentences[sentence_index]
    st.markdown(f'<div class="card"><div class="prompt">{sentence["level"]} · Sentence {sentence_index + 1} of {len(sentences)}</div><h2>{html.escape(sentence["english"])}</h2></div>', unsafe_allow_html=True)
    if st.button("Reveal Spanish", type="primary", use_container_width=True, key="reveal_sentence"):
        st.session_state.sentence_revealed = sentence["id"]
    if st.session_state.get("sentence_revealed") == sentence["id"]:
        st.markdown(f'<div class="card"><div class="answer">{html.escape(sentence["spanish"])}</div></div>', unsafe_allow_html=True)
        st.caption(f'Your status: {progress_label(sentence["id"])}')
        left, right = st.columns(2)
        with left:
            if st.button("Still learning", key="sentence_learning", use_container_width=True):
                if mark_progress(sentence["id"], "learning"):
                    st.session_state.sentence_index = (sentence_index + 1) % len(sentences)
                    st.session_state.sentence_revealed = None
                    st.rerun()
        with right:
            if st.button("Got it ✓", key="sentence_known", type="primary", use_container_width=True):
                if mark_progress(sentence["id"], "known"):
                    st.session_state.sentence_index = (sentence_index + 1) % len(sentences)
                    st.session_state.sentence_revealed = None
                    st.rerun()
    if st.button("Next sentence", key="next_sentence", use_container_width=True):
        st.session_state.sentence_index = (sentence_index + 1) % len(sentences)
        st.session_state.sentence_revealed = None
        st.rerun()

st.divider()
st.markdown('<p class="footnote">Mexican Spanish is the default. Your typed answers are not stored.</p>', unsafe_allow_html=True)
