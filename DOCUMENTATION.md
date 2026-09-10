# LearnHub (djangoFileTTH) — Project Documentation

Educational Django site for BSIT learning demos.  
Repo: https://github.com/irincovictor-cmd/djangoFileTTH  
Local URL (Docker): http://localhost:8081/

This file records what was built, changed, and fixed so you can review the project later.

---

## 1. Project purpose

Simple multi-page educational website:

| Page | Path | Role |
|------|------|------|
| Home | `/`, `/home/` | Hero + CTAs |
| Topics | `/topics/` | List lessons from the database |
| Topic detail | `/topics/<id>/` | Full text + optional external study link |
| About | `/about/` | Project + student info |
| Contact | `/contact/` | ModelForm → save → success page |
| Contact success | `/contact/success/` | Thank-you after valid submit |
| Admin | `/admin/` | Manage Topics, Contacts, Users |

Student: Victor James M. Irinco — BSIT 3rd year, Cristal e-College, Tawala, Panglao, Bohol.

---

## 2. Stack

- **Django** (templates, views, models, admin, forms)
- **Docker Compose** — `web` on port **8081→8000**, optional Postgres / pgAdmin
- **SQLite** by default (`db.sqlite3`) for local/demo data
- **Django REST Framework** in requirements (available; site is mainly HTML, not a JSON API UI)

App package name: **`api`** (this is the Django *app name*, not an external AI API).

---

## 3. Routing (how pages connect)

**Sequence of a request:**

```text
Browser
  → config/urls.py     (include api.urls)
  → api/urls.py        (match path → view)
  → api/views.py       (logic, DB, form)
  → api/templates/     (HTML response)
```

**Main routes (`api/urls.py`):**

```python
path('', views.home, name='home')
path('home/', views.home, name='home_page')
path('topics/', views.topics, name='topics')
path('topics/<int:pk>/', views.topic_detail, name='topic_detail')
path('about/', views.about, name='about')
path('contact/', views.contact, name='contact')
path('contact/success/', views.contact_success, name='contact_success')
```

Guide file: `api/templates/routing_guide.txt`

**Note:** Navbar uses relative paths like `/topics/` so the browser keeps `localhost:8081` (avoids redirects that drop the port).

---

## 4. What we built / changed

### 4.1 Site structure & UI

- Shared layout in `base.html` (navbar, footer, CSS)
- Notebook-style theme (paper background, cards, sticky nav)
- Home hero + CTA buttons
- About page with developer info
- Topics grid; “Ready to practice?” CTA → Contact (centered with `.topics-cta`)
- Fixed CTA alignment (`.page-sub` max-width left-aligned the text while the button centered)

### 4.2 Topics (database-driven)

- **Before:** Static HTML cards only  
- **After:** `Topic` model + list/detail views

Fields: `title`, `tag`, `summary`, `body`, `resource_url`, `resource_label`, `created_at`

- Seed data via migrations (6 starter topics)
- Detail page for each topic
- **Study more** links to official docs (not random pages):

| Topic | Resource |
|-------|----------|
| What is Django? | Django overview docs |
| URLs & Views | Django URL dispatcher |
| HTML with Django | Django templates |
| User input | Django forms |
| Models & migrations | Django migrations |
| Save your work | Official Git documentation |

- Compact underlined resource link (not a huge primary button)

### 4.3 Contact (ModelForm + DB + success redirect)

Aligned with course samples (ModelForm, field loop, success redirect) while keeping LearnHub styling.

| Piece | Role |
|-------|------|
| `Contact` model | `name`, `email`, `contact` (phone), `created_at` |
| `ContactForm` | ModelForm in `api/forms.py` |
| `contact` view | POST → `is_valid()` → **`form.save()`** → `redirect('contact_success')` |
| `contact_success` | Dedicated thank-you page |
| Admin | **Contacts** list for submissions |

**Course sample vs our code:** sample redirect often omits `save()`; we **save then redirect** so Admin still shows rows.

Fields on the form: Name, Email, Contact number (message field removed earlier by request).

### 4.4 Templates inheritance

- `base.html` = shell + CSS  
- Pages only fill `{% block content %}`  
- Contact uses `{% for field in form %}` + `{% csrf_token %}`

---

## 5. Problems fixed

| Issue | Fix |
|-------|-----|
| `TemplateSyntaxError` on `{% url %}` shown as example text in topics | Escaped / rewrote example so Django does not parse it as a tag |
| Home link went to `localhost` without port `:8081` | Avoid bad redirects; serve `/` and `/home/`; use relative `href="/"` |
| Brave forced HTTPS / HSTS on localhost | Browser issue; use Edge or clear HSTS; prefer `http://localhost:8081` |
| Topics CTA “Ready to practice?” not centered | `.topics-cta` flex column + center |
| `no such table: api_topic` | Run `python manage.py migrate` |
| Local `urls.py` “modified” with no logic change | CRLF (`^M`) vs LF — `git restore` then pull |
| Admin login failed | Create user with `createsuperuser` |
| CSRF 403 on POST | Need `{% csrf_token %}`, cookies, refresh form after login |
| Resource button too large on topic detail | Switched to small `.resource-link` text style |

---

## 6. Important files map

```text
config/
  settings.py      # apps, DB, DEBUG
  urls.py          # includes api.urls, admin

api/
  models.py        # Topic, Contact
  forms.py         # ContactForm
  views.py         # page + form logic
  urls.py          # path → view
  admin.py         # Topic + Contact in admin
  migrations/      # 0001 Topic … 0004 Contact
  templates/
    base.html
    home.html, topics.html, topic_detail.html
    about.html, contact.html, contact_success.html
    routing_guide.txt

Dockerfile, docker-compose.yml, requirements.txt
DOCUMENTATION.md   # this file
```

---

## 7. Common commands

```bash
cd ~/djangoFileTTH
git pull origin main

docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose restart web
```

Inspect data:

- Admin → Contacts / Topics  
- `docker compose exec web python manage.py shell` → `from api.models import Contact, Topic`

---

## 8. Design / product notes

- **“Ready to practice?”** = CTA after topics → encourage going to Contact (not a quiz engine)
- Prefer **linking** official docs over scraping third-party sites
- AI/OpenRouter was discussed as optional; **not** required for the graded ModelForm flow
- Deployment checklist (not fully production-hardened): `DEBUG=False`, secret key in env, `ALLOWED_HOSTS`, static files, HTTPS, real Postgres for serious traffic

---

## 9. Mental model (short)

```text
URL  →  View  →  Model/Form/DB  →  Template  →  Browser
```

- **Manual HTML form** = you own every input; save optional  
- **ModelForm** = form tied to model; `is_valid()` + `save()`  
- **Admin “API” section** = app named `api`, not an LLM vendor API  

---

## 10. Changelog summary (high level)

1. Educational multi-page Django site + Docker  
2. Topics from DB + detail + doc links  
3. UI fixes (home port, centering, resource link size, topics template tag)  
4. Contact → ModelForm + `Contact` table + Admin  
5. Contact success redirect (course-style) + `form.save()`  
6. Routing guide + this documentation file  

---

*Generated for analysis and course review. Update this file when you add major features.*
