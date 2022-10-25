#!/usr/bin/env python

import os
import sys


def main() -> None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_project.settings')
    try:
        from django.core import management
    except ImportError:
        raise ImportError('Error importing django')
    management.execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
