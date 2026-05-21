#!/usr/bin/env bash
set -o errexit

# 1. Standard build tasks
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell <<EOF
import os
import json
from django.core.management import call_command
from io import StringIO

data_dump = os.environ.get('INITIAL_DATA_DUMP')
if data_dump:
    print("Found secure data dump environment variable. Processing import...")
    try:
        # Pass the raw text string into Django's loaddata engine natively
        data_stream = StringIO(data_dump)
        call_command('loaddata', '-', format='json', stdin=data_stream)
        print("Secure data migration complete!")
    except Exception as e:
        print(f"Migration error: {e}")
else:
    print("No data dump environment variable found. Skipping.")
EOF