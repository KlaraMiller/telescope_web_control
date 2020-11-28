import os
import django
from django.core.management import execute_from_command_line
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telescope_site_config.settings")
django.setup()

execute_from_command_line(["manage.py", "flush", "--noinput"])
execute_from_command_line(["manage.py", "loaddata", "mydata.json"])
