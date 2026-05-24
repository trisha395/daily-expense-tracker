"""
WSGI config for expense_management_project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_management_project.settings')

application = get_wsgi_application()
