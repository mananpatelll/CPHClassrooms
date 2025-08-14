# CPH Classrooms (PoC)

Server-rendered Django app that lists Temple classrooms by building, shows classroom cards with previews, and a detail page with a Pannellum 360° viewer plus a features table.

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
