# djangoFileTTH

Simple Django + Django REST Framework project with Docker and PostgreSQL.

## What this project does

A small **Notes API** to learn Django:

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/notes/` | List all notes |
| POST | `/api/notes/` | Create a note |
| GET | `/api/notes/1/` | Get one note |
| PUT/PATCH | `/api/notes/1/` | Update a note |
| DELETE | `/api/notes/1/` | Delete a note |

## How the pieces connect

```
HTTP request
    → config/urls.py     (main routes)
    → api/urls.py        (api routes)
    → api/views.py       (NoteViewSet)
    → api/serializers.py (JSON ↔ model)
    → api/models.py      (Note table)
    → PostgreSQL
```

## Quick start

```bash
# Start containers
docker compose up -d

# Run migrations (creates tables)
docker compose exec web python manage.py migrate

# Create admin user (optional)
docker compose exec web python manage.py createsuperuser
```

- API: http://localhost:8081/api/notes/
- Admin: http://localhost:8081/admin/

## Example: create a note

POST to `http://localhost:8081/api/notes/` with JSON:

```json
{
  "title": "My first note",
  "body": "Hello Django!"
}
```

Or use the browsable API form in the browser at `/api/notes/`.
