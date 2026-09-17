# Portfolio + Contact (Django) — pull & run

## Ready on GitHub

- **Contact** model: `name`, `email`, `message`
- Migration **0005** (phone → message)
- Form + `/contact/` saves to DB
- **Admin → Contacts**
- `/` and `/portfolio/` use `portfolio.html`

## Commands

```bash
cd ~/djangoFileTTH
git pull origin main
docker compose up -d
docker compose exec web python manage.py migrate
```

Superuser (if needed):

```bash
docker compose exec web python manage.py createsuperuser
```

## Test

- http://localhost:8081/contact/
- http://localhost:8081/admin/ → Contacts
- http://localhost:8081/

## Your HTML later

Replace `api/templates/portfolio.html`.  
If contact is embedded, POST to `{% url 'contact' %}` with `{% csrf_token %}` and fields `name`, `email`, `message`.
