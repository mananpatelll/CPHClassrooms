# CPH Classrooms (PoC)
This project, developed under Temple University's Classroom Technology Department, is designed to provide detailed information about each classroom, manage classroom scheduling, and offer technology support directly through TUportal. The goal is to make these services more accessible for faculty and students while creating a centralized hub for all classroom technology–related resources.
Tech: Python 3.11, Django 5, Bootstrap 5 (templates), Pannellum (360 viewer). SQLite for dev; Postgres-ready.

## Quick start

```bash
# create & activate venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# migrate DB
python manage.py migrate

# (optional) import classrooms
python manage.py import_classrooms --path feed.json

# run dev server
python manage.py runserver
