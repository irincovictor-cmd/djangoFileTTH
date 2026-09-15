# Contact form — full beginner guide (Django)

This guide explains **how we built the Contact feature** in **djangoFileTTH (LearnHub)** as if you are new to Django.

You can use it to **study** and to **rebuild the same idea** on your midterm.

---

## Table of contents

1. [What is Django, in simple words?](#1-what-is-django-in-simple-words)
2. [The big picture of our Contact feature](#2-the-big-picture-of-our-contact-feature)
3. [Project layout (where files live)](#3-project-layout-where-files-live)
4. [Step 0 — Make sure Django can run](#4-step-0--make-sure-django-can-run)
5. [Step 1 — Model (the database table)](#5-step-1--model-the-database-table)
6. [Step 2 — Migration (create the table for real)](#6-step-2--migration-create-the-table-for-real)
7. [Step 3 — ModelForm (the form tied to the model)](#7-step-3--modelform-the-form-tied-to-the-model)
8. [Step 4 — Views (what happens when you open the page)](#8-step-4--views-what-happens-when-you-open-the-page)
9. [Step 5 — URLs (connecting addresses to views)](#9-step-5--urls-connecting-addresses-to-views)
10. [Step 6 — Templates (the HTML the user sees)](#10-step-6--templates-the-html-the-user-sees)
11. [Step 7 — Admin (see saved data in the browser)](#11-step-7--admin-see-saved-data-in-the-browser)
12. [Settings you must not forget](#12-settings-you-must-not-forget)
13. [Full request walk-through (slow motion)](#13-full-request-walk-through-slow-motion)
14. [Manual form vs ModelForm](#14-manual-form-vs-modelform)
15. [Common errors and how to fix them](#15-common-errors-and-how-to-fix-them)
16. [Commands cheat sheet](#16-commands-cheat-sheet)
17. [Minimal code you can copy](#17-minimal-code-you-can-copy)
18. [Oral defense one-liners](#18-oral-defense-one-liners)

---

## 1. What is Django, in simple words?

**Django** is a **Python web framework**.  
It helps you build websites without writing everything from zero.

Think of a website like a restaurant:

| Restaurant | Django |
|------------|--------|
| Menu (URLs) | `urls.py` — which address goes where |
| Kitchen (logic) | `views.py` — what to do |
| Recipes / storage (data) | `models.py` — tables in the database |
| Plates (what the customer sees) | `templates/` — HTML pages |
| Order form | `forms.py` — collect and check user input |

### MVT (Django’s pattern)

People say Django uses **MVT**:

- **M**odel → data (database)
- **V**iew → Python logic
- **T**emplate → HTML

Flow:

```text
Browser asks for a URL
    → urls.py picks a view
    → view may load a model / form
    → view returns a template (HTML)
    → browser shows the page
```

---

## 2. The big picture of our Contact feature

We wanted a page where someone types:

- **Name**
- **Email**
- **Contact number** (phone)

Then we:

1. **Check** the data is valid  
2. **Save** it in the database  
3. **Redirect** to a “success” page  
4. Allow the teacher/you to see rows in **Django Admin**

### Happy path

```text
GET  /contact/           → show empty form
POST /contact/           → user presses Submit
                         → form is valid?
                            yes → save to DB → go to /contact/success/
                            no  → show same page with errors
GET  /contact/success/   → “Message sent” page
```

---

## 3. Project layout (where files live)

Our app is named **`api`** (just a folder name — not “AI API”).

```text
djangoFileTTH/
├── config/                 # project settings + main urls
│   ├── settings.py         # apps, database, DEBUG, etc.
│   └── urls.py             # includes api.urls + admin
├── api/                    # our app
│   ├── models.py           # Topic, Contact
│   ├── forms.py            # ContactForm
│   ├── views.py            # home, topics, contact, ...
│   ├── urls.py             # paths like contact/
│   ├── admin.py            # Admin registration
│   ├── migrations/         # database change history
│   └── templates/          # HTML files
│       ├── base.html
│       ├── contact.html
│       └── contact_success.html
├── manage.py
├── docker-compose.yml
└── docs/
    └── CONTACT_FORM_GUIDE.md   ← this file
```

**Remember:**  
- **Project** = whole folder (`config`, `manage.py`)  
- **App** = one feature package (`api`)

---

## 4. Step 0 — Make sure Django can run

In our class setup we used **Docker**. Concept is the same without Docker.

### With Docker (our project)

```bash
cd ~/djangoFileTTH
docker compose up -d
```

Site: **http://localhost:8081/**

### Ideas you need before coding Contact

1. App is listed in `INSTALLED_APPS` in `settings.py` (ours is `'api'`).
2. Main `config/urls.py` includes the app urls, for example:

```python
path('', include('api.urls')),
path('admin/', admin.site.urls),
```

3. Database exists (SQLite file or Postgres). Migrations create **tables** inside it.

If the site already opens Home / Topics, Step 0 is done.

---

## 5. Step 1 — Model (the database table)

### What is a model?

A **model** is a Python class that describes a **table**.

- Class name ≈ table (Django often names it `api_contact`)
- Class attributes ≈ **columns**
- One object ≈ one **row**

### Our Contact model

In `api/models.py`:

```python
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(
        max_length=30,
        verbose_name="Contact number",
        help_text="Phone or mobile number",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f"{self.name} ({self.email})"
```

### Field types (simple)

| Field | Meaning |
|-------|--------|
| `CharField` | Short text (needs `max_length`) |
| `EmailField` | Text that should look like an email |
| `DateTimeField(auto_now_add=True)` | Set automatically when the row is created |

`verbose_name` is the **label** humans see on forms/admin.  
`__str__` is how the object prints in Admin (readable name).

**You only wrote Python here.** The real table appears after migrations.

---

## 6. Step 2 — Migration (create the table for real)

### Why migrations?

Django does **not** magically change the database when you edit `models.py`.  
You must:

1. **makemigrations** — write a plan (“create table Contact…”)  
2. **migrate** — apply the plan to the database  

### Commands (Docker)

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

In our repo this created something like `api/migrations/0004_contact.py`.

### If you skip migrate

You will see errors like:

```text
no such table: api_contact
```

That means: model exists in Python, **table does not exist** in the DB yet.

---

## 7. Step 3 — ModelForm (the form tied to the model)

### What is a form in Django?

A form:

- Builds input fields  
- Checks data (`is_valid()`)  
- Can save to the database (`save()`) when it is a **ModelForm**

### Our form — `api/forms.py`

```python
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "contact"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }),
            "contact": forms.TextInput(attrs={
                "placeholder": "e.g. 09XX XXX XXXX",
                "inputmode": "tel",
                "autocomplete": "tel",
            }),
        }
```

### What each part means

| Part | Meaning |
|------|--------|
| `forms.ModelForm` | Form connected to a model |
| `model = Contact` | Use Contact’s fields |
| `fields = [...]` | Only these columns appear on the form |
| `widgets` | Optional HTML attributes (placeholder, etc.) |

**Note:** Field names must match the model (`contact`, not `contact_number`) unless you rename carefully.

We do **not** put design CSS inside `forms.py`. Design lives in templates / CSS.

---

## 8. Step 4 — Views (what happens when you open the page)

A **view** is a Python function (or class) that:

- Receives the **request**  
- Decides what to do  
- Returns a **response** (usually HTML)

### Contact views — `api/views.py`

```python
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        # User submitted the form
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # write a row into the Contact table
            return redirect('contact_success')
    else:
        # User just opened the page
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')
```

### Line-by-line ideas

| Code | Meaning |
|------|--------|
| `request.method == 'POST'` | Browser sent form data |
| `ContactForm(request.POST)` | Fill form with submitted values |
| `form.is_valid()` | Check rules (required, email format, …) |
| `form.save()` | INSERT into database |
| `redirect('contact_success')` | Send user to success URL (by **name**) |
| `render(..., {'form': form})` | Show template and pass the form object |

### Critical teaching point

Some class samples only:

```python
return redirect('contact_success')
```

without `form.save()`.  
Then the success page shows, but **Admin is empty**.  
If the goal is “store the message,” you **must** call `save()`.

---

## 9. Step 5 — URLs (connecting addresses to views)

### App urls — `api/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    # ... other pages ...
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
]
```

| Piece | Meaning |
|-------|--------|
| `'contact/'` | Path after the site root |
| `views.contact` | Function to call |
| `name='contact'` | Nickname used in `redirect()` and `{% url %}` |

### Project urls — `config/urls.py`

Must include the app, for example:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
```

So full addresses become:

- http://localhost:8081/contact/  
- http://localhost:8081/contact/success/  
- http://localhost:8081/admin/  

---

## 10. Step 6 — Templates (the HTML the user sees)

### Template inheritance

- `base.html` = shared layout (nav, footer, CSS)  
- `contact.html` = only the contact **content** block  

That keeps pages consistent.

### Contact form template (logic version — minimal)

```django
<form method="post" action="{% url 'contact' %}">
    {% csrf_token %}

    {% for field in form %}
        <div>
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}
                <div>{{ field.errors }}</div>
            {% endif %}
        </div>
    {% endfor %}

    <button type="submit">Submit</button>
</form>
```

### Why each part matters

| Part | Why |
|------|-----|
| `method="post"` | Send data in the request body (not in the URL) |
| `{% csrf_token %}` | Security token — **required** or Django returns **403** |
| `{% for field in form %}` | Auto-build inputs from ContactForm |
| `{{ field }}` | The input widget |
| `field.errors` | Show validation messages |

### Design vs logic

- **Guide / midterm logic** = structure above (simple).  
- **LearnHub pretty UI** = extra CSS classes in `base.html` / `contact.html` (glass card, colors).  

Same form engine; design is optional clothing.

### Success page

`contact_success.html` does **not** need the form.  
It only says “thanks” and links back home or to contact again.

---

## 11. Step 7 — Admin (see saved data in the browser)

Django Admin is a built-in control panel.

### Register the model — `api/admin.py`

```python
from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'created_at')
    search_fields = ('name', 'email', 'contact')
```

### Create a login once

```bash
docker compose exec web python manage.py createsuperuser
```

Then open http://localhost:8081/admin/ → **Contacts**.

Each successful form submit should add a row there (because of `form.save()`).

---

## 12. Settings you must not forget

In `config/settings.py` (concepts):

| Setting | Why it matters for Contact |
|---------|----------------------------|
| `INSTALLED_APPS` includes `'api'` | Django loads your models/forms |
| `INSTALLED_APPS` includes `'django.contrib.admin'` | Admin works |
| Database configured | `migrate` and `save()` have somewhere to write |
| Middleware includes CSRF | Forms stay protected |

You usually do **not** turn CSRF off for normal school forms.

---

## 13. Full request walk-through (slow motion)

### Opening the form (GET)

1. Browser goes to `/contact/`  
2. `api/urls.py` calls `views.contact`  
3. Method is GET → `form = ContactForm()` (empty)  
4. `render(request, 'contact.html', {'form': form})`  
5. Template loops fields → user sees blank inputs  

### Submitting (POST)

1. User clicks Submit  
2. Browser POSTs to `/contact/` including CSRF token + fields  
3. View builds `ContactForm(request.POST)`  
4. `is_valid()` runs  
   - Invalid → same template, errors shown  
   - Valid → `form.save()` inserts row → `redirect('contact_success')`  
5. Browser requests `/contact/success/`  
6. `contact_success` view returns thank-you HTML  

---

## 14. Manual form vs ModelForm

| Manual HTML form | ModelForm (what we use) |
|------------------|-------------------------|
| You write every `<input name="name">` | Form generated from model |
| You read `request.POST.get('name')` yourself | `form.cleaned_data` / `save()` |
| Easy to forget a field | Fields stay aligned with the table |
| Fine for tiny demos | Better for school “save to DB” tasks |

We moved from a simple demo form to **ModelForm + database** to match the course pattern.

---

## 15. Common errors and how to fix them

| Error / symptom | Likely cause | Fix |
|-----------------|--------------|-----|
| **403 CSRF verification failed** | Missing `{% csrf_token %}` or stale page | Add token; refresh; allow cookies |
| **no such table: api_contact** | Forgot migrate | `python manage.py migrate` |
| Success page but **empty Admin** | Forgot `form.save()` | Save before redirect |
| **NoReverseMatch** | Wrong redirect name | Use `name='contact_success'` in urls |
| Form fields missing | `fields = [...]` incomplete | Match model field names |
| Admin has no Contacts | Not registered | `@admin.register(Contact)` |
| Changes not showing | Old container / no pull | `git pull`, restart web |

---

## 16. Commands cheat sheet

```bash
cd ~/djangoFileTTH
git pull origin main

# start
docker compose up -d

# database
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# admin user
docker compose exec web python manage.py createsuperuser

# optional restart
docker compose restart web
```

Pages:

- Form: http://localhost:8081/contact/  
- Success: http://localhost:8081/contact/success/  
- Admin: http://localhost:8081/admin/  

---

## 17. Minimal code you can copy

This is the **simplest working set** (no fancy CSS).

### models.py (Contact only)

```python
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=30, verbose_name="Contact number")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

### forms.py

```python
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "contact"]
```

### views.py (contact parts)

```python
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_success")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})

def contact_success(request):
    return render(request, "contact_success.html")
```

### urls.py (add these)

```python
path("contact/", views.contact, name="contact"),
path("contact/success/", views.contact_success, name="contact_success"),
```

### contact.html (minimal)

```django
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Send</button>
</form>
```

(`form.as_p` is the shortest way to render fields. Our project uses a `{% for field in form %}` loop for more control.)

### admin.py

```python
from django.contrib import admin
from .models import Contact

admin.site.register(Contact)
```

Then: **makemigrations → migrate → runserver (or Docker) → test.**

---

## 18. Oral defense one-liners

**What is a model?**  
“A Python class that describes a database table.”

**What is a ModelForm?**  
“A form built from a model so validation and saving match the table.”

**What does the contact view do?**  
“On GET it shows an empty form; on POST it validates, saves, and redirects to a success page.”

**Why csrf_token?**  
“So Django can reject fake cross-site form posts.”

**Why migrate?**  
“So the database table actually exists after we define the model.”

---

## Final mental picture

```text
URL  →  View  →  Form + Model  →  Database
              ↘
                Template (HTML)
```

That is the whole Contact feature in Django — same idea as our LearnHub project, with or without pretty CSS.

---

*Written for BSIT study / midterm recreation. Matches djangoFileTTH contact flow.*
