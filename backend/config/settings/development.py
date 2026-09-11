import os

from .base import *  # noqa: F403

DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"
