# -*- coding: utf-8 -*-
from django.contrib.sessions.backends.base import SessionBase, CreateError
from utils.sessions import database as db


class SessionStore(SessionBase):
    """
    Implements Redis session store.
    """

    def exists(self, session_key):
        if db.exists("session:%s" % session_key):
            return True
        return False

    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                # The key wasn't unique, try again
                continue
            return

    def save(self, must_create=False):
        if must_create:
            func = db.setnx
        else:
            func = db.set
        key = "session:%s" % self.session_key
        result = func(
                key,
                self.encode(self._get_session(no_load=must_create)))
        if must_create and result is None:
            raise CreateError
        # The key has been set, set its expiration
        db.expire(key, self.get_expiry_age())
        self.modified = False

    def delete(self, session_key=None):
        if session_key is None:
            session_key = self.session_key
        db.delete("session:%s" % session_key)

    def load(self):
        session_data = db.get("session:%s" % self.session_key)
        if session_data is None:
            self.create()
            return {}
        return self.decode(session_data)
