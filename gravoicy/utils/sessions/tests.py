# -*- coding: utf-8 -*-
from django.test import TestCase
from redis_sessions.backends.redis import SessionStore


class RedisSessionTest(TestCase):
    """
    Redis Session Backends Test
    """
    def test_session_store(self):
        """
        Tests session store creation.
        """
        st = SessionStore()
        st.load()
        session_key = st.session_key

        self.assertEqual(st.exists(session_key), True)
        self.assertEqual(st.exists("whatever"), False)

        st["data1"] = "Hello world!"
        st["data2"] = "my data"
        self.assertEqual(st.modified, True)
        st.save()
        self.assertEqual(st.modified, False)

        st2 = SessionStore(session_key)
        self.assertEqual(st.session_key, session_key)
        self.assertEqual(st2["data1"], "Hello world!")
        self.assertEqual(st2["data2"], "my data")

        st2.delete()
        st2.load()
        self.assertNotEqual(st2.session_key, session_key)
