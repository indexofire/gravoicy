# -*- coding: utf-8 -*-
from django.conf import settings
from redis import client


database = client.Redis(
    host     = getattr(settings, "REDIS_HOST", "localhost"),
    port     = getattr(settings, "REDIS_PORT", 6379),
    db       = getattr(settings, "REDIS_DB", 0),
    password = getattr(settings, "REDIS_PASSWORD", ""),
)
