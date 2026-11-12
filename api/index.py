"""
Vercel serverless entry point for the Godfred's Fashion Shop Django app.

Vercel's Python runtime auto-discovers a WSGI application called ``application``
(or ``app``) in files such as ``api/index.py`` and wraps it as a serverless
function. Every HTTP request is routed here (see ``vercel.json``) and Django
handles URL dispatching exactly as it does locally.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopnow.settings')

application = get_wsgi_application()
