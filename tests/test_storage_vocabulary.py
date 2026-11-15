import unittest
from types import SimpleNamespace

from storage import (
    ProgressStore,
    load_config,
    request_email_code,
    verified_user_id,
    verify_email_code,
)
from vocabulary import CATEGORIES, LEVELS, VOCABULARY, filter_words, summarize_progress


class FakeQuery:
    def __init__(self, database, table):
        self.database = database
        self.table_name = table
        self.action = "select"
        self.filters = {}
        self.payload = None

    def select(self, columns):
        self.action = "select"
        return self

    def upsert(self, payload, on_conflict=None):
        self.action = "upsert"
        self.payload = dict(payload)
        return self

    def delete(self):
        self.action = "delete"
        return self

    def eq(self, field, value):
        self.filters[field] = value
        return self

    def execute(self):
        if self.action == "select":
            rows = [dict(row) for row in self.database.rows.values()
                    if row["user_id"] == self.filters.get("user_id")]
            return SimpleNamespace(data=rows)
        if self.action == "upsert":
            key = (self.payload["user_id"], self.payload["word_id"])
            self.database.rows[key] = dict(self.payload)
            return SimpleNamespace(data=[dict(self.payload)])
        removed = []
        for key, row in list(self.database.rows.items()):
            if all(row.get(field) == value for field, value in self.filters.items()):
                removed.append(self.database.rows.pop(key))
        return SimpleNamespace(data=removed)


class FakeDatabase:
    def __init__(self):
        self.rows = {}

    def table(self, table_name):
        if table_name != "word_progress":
            raise AssertionError("Unexpected table")
        return FakeQuery(self, table_name)


class FakeAuth:
    def __init__(self):
        self.request = None
        self.verified = None

    def sign_in_with_otp(self, payload):
        self.request = payload
        return SimpleNamespace()

    def verify_otp(self, payload):
        self.verified = payload
        session = SimpleNamespace(access_token="access-test", refresh_token="refresh-test")
        return SimpleNamespace(session=session)

    def get_user(self):
        return SimpleNamespace(user=SimpleNamespace(id="user-a"))


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.db = FakeDatabase()
        self.client = self.db
        self.user_a = ProgressStore(self.client, "user-a")
        self.user_b = ProgressStore(self.client, "user-b")

    def test_save_load_update_and_delete(self):
        self.user_a.save("agua", "learning", "2026-11-14T10:00:00+00:00")
        self.assertEqual(self.user_a.load()["agua"]["status"], "learning")
        self.user_a.save("agua", "known", "2026-11-14T11:00:00+00:00")
        self.assertEqual(len(self.db.rows), 1)
        self.assertEqual(self.user_a.load()["agua"]["status"], "known")
        self.assertTrue(self.user_a.delete("agua"))
        self.assertEqual(self.user_a.load(), {})

    def test_progress_is_scoped_to_the_store_user(self):
        self.user_a.save("agua", "known")
        self.user_b.save("agua", "learning")
        self.assertEqual(self.user_a.load()["agua"]["status"], "known")
        self.assertEqual(self.user_b.load()["agua"]["status"], "learning")
        self.assertEqual(len(self.db.rows), 2)

    def test_a_new_store_instance_reloads_persisted_backend_state(self):
        self.user_a.save("manzana", "known")
        reopened_store = ProgressStore(self.client, "user-a")
        self.assertEqual(reopened_store.load()["manzana"]["status"], "known")

    def test_invalid_progress_is_rejected(self):
        with self.assertRaises(ValueError):
            self.user_a.save("agua", "mastered")
        with self.assertRaises(ValueError):
            ProgressStore(self.client, "")

    def test_secret_config_and_environment_config(self):
        config = load_config(
            {"supabase": {"url": "https://example.supabase.co", "publishable_key": "sb_publishable_test", "allowed_email": "Me@Example.com"}},
            {},
        )
        self.assertEqual(config.allowed_email, "me@example.com")
        self.assertEqual(config.url, "https://example.supabase.co")
        env_config = load_config({}, {
            "SUPABASE_URL": "https://env.supabase.co",
            "SUPABASE_PUBLISHABLE_KEY": "sb_publishable_env",
            "CALABAZA_ALLOWED_EMAIL": "me@example.com",
        })
        self.assertEqual(env_config.url, "https://env.supabase.co")
        self.assertIsNone(load_config({}, {}))

    def test_service_role_key_is_rejected(self):
        with self.assertRaises(ValueError):
            load_config({"supabase": {
                "url": "https://example.supabase.co",
                "publishable_key": "sb_secret_do_not_use",
                "allowed_email": "me@example.com",
            }}, {})

    def test_email_login_disables_self_signup_and_keeps_session_tokens(self):
        auth = FakeAuth()
        client = SimpleNamespace(auth=auth)
        request_email_code(client, "me@example.com")
        self.assertFalse(auth.request["options"]["should_create_user"])
        tokens = verify_email_code(client, "me@example.com", "123456")
        self.assertEqual(tokens, {"access_token": "access-test", "refresh_token": "refresh-test"})
        self.assertEqual(verified_user_id(client), "user-a")


class VocabularyTests(unittest.TestCase):
    def test_catalog_has_unique_ids_and_all_levels_and_categories(self):
        ids = [word["id"] for word in VOCABULARY]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual({word["level"] for word in VOCABULARY}, set(LEVELS))
        self.assertEqual(set(CATEGORIES), {word["category"] for word in VOCABULARY})

    def test_filtering_by_level_category_and_accent_insensitive_search(self):
        result = filter_words(level=LEVELS[0], category="Food & drink", query="cafe")
        self.assertEqual([word["id"] for word in result], ["cafe"])
        self.assertTrue(filter_words(query="where"))
        self.assertTrue(filter_words(category="Question words"))

    def test_progress_summary_for_a_group(self):
        words = filter_words(level=LEVELS[0], category="Greetings & courtesy")
        progress = {"hola": {"status": "known"}, "gracias": {"status": "learning"}}
        self.assertEqual(summarize_progress(words, progress), {
            "total": 4, "known": 1, "learning": 1, "new": 2
        })


if __name__ == "__main__":
    unittest.main()
