# LearnHub (djangoFileTTH) — Project Documentation

Educational Django site for BSIT learning demos.  
Repo: https://github.com/irincovictor-cmd/djangoFileTTH  
Local URL (Docker): http://localhost:8081/

This file records what was built, changed, and fixed so you can review the project later.

---

## 1. Project purpose

Simple multi-page educational website (LearnHub) plus a Portfolio site under `/portfolio/`.

| Page | Path | Role |
|------|------|------|
| Home | `/`, `/home/` | Hero + CTAs |
| Topics | `/topics/` | List lessons from the database; add modal; recycle bin |
| Topic detail | `/topics/<id>/` | Full text + optional external study link |
| Topic edit | `/topics/<id>/edit/` | Update an active topic |
| About | `/about/` | Project + student info |
| Contact | `/contact/` | LearnHub messages → Contact table |
| Portfolio contact | `/portfolio/contact/` | Portfolio messages → Profile table |
| Admin | `/admin/` | Topics, Contacts, Profiles, Users |

Student: Victor James M. Irinco — BSIT 3rd year, Cristal e-College, Tawala, Panglao, Bohol.

---

## 2. Stack

- **Django** (templates, views, models, admin, forms)
- **Docker Compose** — `web` on port **8081→8000**, optional Postgres / pgAdmin
- **SQLite** by default (`db.sqlite3`) for local/demo data
- **Django REST Framework** in requirements (available; site is mainly HTML)

App package name: **`api`**.

---

## 3. Routing

```text
Browser → config/urls.py → api/urls.py → api/views.py → templates
```

Important topic routes:

```python
path('topics/', views.topics, name='topics')
path('topics/manage/', views.topic_manage, name='topic_manage')
path('topics/<int:pk>/edit/', views.topic_edit, name='topic_edit')
path('topics/<int:pk>/', views.topic_detail, name='topic_detail')
```

`edit` is registered **before** `topics/<pk>/` so the path segment is not treated as an id.

---

## 4. Topics system (current)

### Model fields (`Topic`)

`title`, `tag`, `summary`, `body`, `resource_url`, `resource_label`, `created_at`, `deleted_at`

- **Active topics:** `deleted_at` is null → shown on `/topics/`
- **Recycle bin:** `deleted_at` set → soft-deleted; restore or permanent delete

### Already present (kept intact)

- List (card grid)
- Detail page
- Add via modal (`TopicManageForm` + `topic_manage`)
- Soft-delete → recycle bin
- Restore / permanent delete from bin
- LearnHub notebook styling

### Integrated: Topic Edit (from reference idea)

**Source idea:** reference `topic_edit` (load topic → form → save → redirect).  
**Not a full replace** of Hannah’s Tailwind app or hard-delete confirm flow.

| Item | Detail |
|------|--------|
| **What was added** | Edit active topics only |
| **URL** | `/topics/<pk>/edit/` (`name='topic_edit'`) |
| **View** | `topic_edit` in `api/views.py` |
| **Form** | `TopicEditForm` (ModelForm) in `api/forms.py` |
| **Template** | `api/templates/learnhub/topic_edit.html` (extends LearnHub `base.html`) |
| **Entry point** | **Edit topic** button on topic detail page |
| **After save** | Redirect to topic detail + success message |
| **How it fits** | Uses existing `Topic` fields; does not touch soft-delete/bin/add modal |
| **Field mapping vs reference** | reference `name/category/description` → our `title/tag/summary` (+ body, links) |

**Files changed for this feature:**

- `api/forms.py` — added `TopicEditForm`
- `api/views.py` — added `topic_edit`
- `api/urls.py` — added `topics/<pk>/edit/`
- `api/templates/learnhub/topic_edit.html` — new
- `api/templates/learnhub/topic_detail.html` — Edit button
- `DOCUMENTATION.md` — this section

---

## 5. Contact / Profile separation

| Site | Path | Table |
|------|------|--------|
| LearnHub | `/contact/` | `Contact` (messages) |
| Portfolio | `/portfolio/contact/` | `Profile` (person + last message) |

Do not mix these flows.

---

## 6. Common commands

```bash
cd ~/djangoFileTTH
git pull origin main
docker compose up -d
docker compose exec web python manage.py migrate
docker compose restart web
```

Open: http://localhost:8081/topics/ → open a topic → **Edit topic**.

---

## 7. Integration policy (team plan)

1. Keep existing djangoFileTTH intact — no wholesale replace with reference code.
2. Compare reference vs repo; integrate **missing** features only.
3. One feature at a time; adapt to existing architecture and field names.
4. Document each integration in this file.

**Next candidates (not done yet):** optional search on topics list; optional confirm UI before soft-delete/purge (only if desired without removing recycle bin).

---

*Update this file when you add major features.*
