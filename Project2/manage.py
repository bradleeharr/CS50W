#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')
    execute_from_command_line([sys.argv[0], 'makemigrations'])
    execute_from_command_line([sys.argv[0], 'migrate'])
    execute_from_command_line([sys.argv[0], 'runserver', '8080'])


if __name__ == '__main__':
    main()
