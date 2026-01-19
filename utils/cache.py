import time


class TTLCache:
    def __init__(self, max_items=256):
        self.max_items = max_items
        self._data = {}

    def get(self, key):
        record = self._data.get(key)
        if not record:
            return None
        value, expires_at = record
        if expires_at and expires_at < time.time():
            self._data.pop(key, None)
            return None
        return value

    def set(self, key, value, ttl=None):
        if len(self._data) >= self.max_items:
            self._data.pop(next(iter(self._data)), None)
        expires_at = time.time() + ttl if ttl else None
        self._data[key] = (value, expires_at)
