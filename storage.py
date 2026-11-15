"""Supabase Auth and per-user progress storage for Calabaza.

The client is deliberately created per Streamlit session; never cache an
authenticated Supabase client globally because its auth state is user-specific.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping, Optional


@dataclass(frozen=True)
class SupabaseConfig:
    url: str
    publishable_key: str
    allowed_email: str


def load_config(secrets=None, environ=None):
    """Read app credentials from Streamlit secrets or environment variables."""
    secrets = secrets or {}
    environ = environ or {}
    nested = secrets.get("supabase", {}) if hasattr(secrets, "get") else {}

    def pick(secret_name, env_name):
        return (nested.get(secret_name) if hasattr(nested, "get") else None) or environ.get(env_name)

    url = pick("url", "SUPABASE_URL")
    key = pick("publishable_key", "SUPABASE_PUBLISHABLE_KEY")
    email = pick("allowed_email", "CALABAZA_ALLOWED_EMAIL")
    if not url or not key or not email:
        return None
    if not str(key).startswith("sb_publishable_"):
        raise ValueError("Use a Supabase publishable key; secret/service-role keys are not supported.")
    return SupabaseConfig(str(url).rstrip("/"), str(key), str(email).strip().casefold())


def create_user_client(config, session=None):
    """Create an uncached client and, if supplied, attach this user's session."""
    if config is None:
        raise ValueError("Supabase is not configured.")
    from supabase import create_client

    client = create_client(config.url, config.publishable_key)
    if session:
        client.auth.set_session(session["access_token"], session["refresh_token"])
    return client


def request_email_code(client, email):
    """Send an OTP only to an existing account; public sign-up stays disabled."""
    return client.auth.sign_in_with_otp({
        "email": email.strip(),
        "options": {"should_create_user": False},
    })


def verify_email_code(client, email, code):
    response = client.auth.verify_otp({
        "email": email.strip(),
        "token": code.strip(),
        "type": "email",
    })
    session = getattr(response, "session", None)
    if session is None and isinstance(response, Mapping):
        session = response.get("session")
    if not session:
        raise ValueError("The code was not accepted. Request a new code and try again.")
    access_token = getattr(session, "access_token", None)
    refresh_token = getattr(session, "refresh_token", None)
    if isinstance(session, Mapping):
        access_token = session.get("access_token", access_token)
        refresh_token = session.get("refresh_token", refresh_token)
    if not access_token or not refresh_token:
        raise ValueError("Sign-in did not return a usable session.")
    return {"access_token": access_token, "refresh_token": refresh_token}


def verified_user_id(client):
    """Return the user ID from Supabase Auth's verified-user endpoint."""
    response = client.auth.get_user()
    user = getattr(response, "user", None)
    if user is None and isinstance(response, Mapping):
        user = response.get("user")
    user_id = getattr(user, "id", None)
    if user_id is None and isinstance(user, Mapping):
        user_id = user.get("id")
    if not user_id:
        raise ValueError("No verified signed-in user is available.")
    return str(user_id)


class ProgressStore:
    """Persist only a user's card status and last review timestamp."""

    def __init__(self, client, user_id):
        if not user_id:
            raise ValueError("A verified user ID is required.")
        self.client = client
        self.user_id = str(user_id)

    def load(self):
        response = (
            self.client.table("word_progress")
            .select("word_id,status,last_reviewed_at")
            .eq("user_id", self.user_id)
            .execute()
        )
        rows = getattr(response, "data", None)
        if rows is None and isinstance(response, Mapping):
            rows = response.get("data", [])
        return {row["word_id"]: row for row in (rows or [])}

    def save(self, word_id, status, reviewed_at=None):
        if not word_id or status not in {"learning", "known"}:
            raise ValueError("A word ID and valid progress status are required.")
        if reviewed_at is None:
            reviewed_at = datetime.now(timezone.utc).isoformat()
        payload = {
            "user_id": self.user_id,
            "word_id": str(word_id),
            "status": status,
            "last_reviewed_at": reviewed_at,
        }
        self.client.table("word_progress").upsert(
            payload, on_conflict="user_id,word_id"
        ).execute()
        return payload

    def delete(self, word_id):
        response = (
            self.client.table("word_progress")
            .delete()
            .eq("user_id", self.user_id)
            .eq("word_id", str(word_id))
            .execute()
        )
        rows = getattr(response, "data", None)
        if rows is None and isinstance(response, Mapping):
            rows = response.get("data", [])
        return bool(rows)
