#!/usr/bin/env bash
set -o errexit

# 1. Standard build tasks
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell <<EOF
import os
from django.core.management import call_command

data_dump = os.environ.get('INITIAL_DATA_DUMP')
if data_dump and len(data_dump) > 5:
    print("Found secure data dump environment variable. Processing import...")
    try:
        # Create a temporary local file on Render's build environment
        temp_filename = 'temp_prod_dump.json'
        with open(temp_filename, 'w', encoding='utf-8') as f:
            f.write(data_dump)
        
        # Load the file securely using standard Django utility pathways
        call_command('loaddata', temp_filename)
        print("Secure data migration complete!")
        
        # Clean up and destroy the temporary file immediately for absolute security
        os.remove(temp_filename)
        print("Temporary migration files purged successfully.")
    except Exception as e:
        print(f"Migration error: {e}")
else:
    print("No data dump environment variable found or string format empty. Skipping.")
EOF