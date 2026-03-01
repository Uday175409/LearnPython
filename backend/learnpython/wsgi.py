"""
WSGI config for learnpython project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnpython.settings')

# Run migrations and seed automatically on startup.
# This is essential on platforms like Render's free tier where the
# filesystem is ephemeral — the SQLite DB is wiped on every spin-up,
# so migrations must run before the first request is served.
def _run_startup_tasks():
    try:
        from django.core.management import call_command
        call_command("migrate", "--run-syncdb", verbosity=1)
        call_command("seed", verbosity=1)
    except Exception as exc:  # noqa: BLE001
        import logging
        logging.getLogger(__name__).error("Startup tasks failed: %s", exc)

_run_startup_tasks()

application = get_wsgi_application()
