# Contact form — how we built it (midterm study guide)

Project: **djangoFileTTH** (LearnHub)  
Goal: recreate the same pattern on your midterm — **Model → Form → View → Template → migrate → Admin**

Local URL: http://localhost:8081/contact/

---

## 1. Big picture (what “contact” does)

```text
User opens /contact/
    GET  → empty ContactForm → contact.html
    POST → validate → form.save() → redirect → /contact/success/
```

Data is stored in the **Contact** table and visible in **Django Admin → Contacts**.

---

## 2. Pieces you need (checklist)

| # | File | Purpose |
|---|------|--------|
| 1 | `api/models.py` | `Contact` model = database table |
| 2 | migration | Creates table `api_contact` |
| 3 | `api/forms.py` | `ContactForm` (ModelForm) |
| 4 | `api/views.py` | `contact` + `contact_success` |
| 5 | `api/urls.py` | routes for both pages |
| 6 | `contact.html` | form UI + `{% csrf_token %}` |
| 7 | `contact_success.html` | thank-you page |
| 8 | `api/admin.py` | register Contact so you can see rows |

---

## 3. Step-by-step (recreate from scratch)

### Step A — Model (`api/models.py`)

```python
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
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
```

**Meaning:** one row per submission — name, email, phone, timestamp.

---

### Step B — Migration

```bash
# inside Docker for this project:
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

We already have `api/migrations/0004_contact.py` in the repo.  
If the table is missing: run `migrate`.

---

### Step C — ModelForm (`api/forms.py`)

```python
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "contact"]
        # optional: widgets for placeholders
```

**Why ModelForm?**  
Fields come from the model → `is_valid()` + `form.save()` writes to the DB.  
No need to hand-map every `request.POST` field.

---

### Step D — Views (`api/views.py`)

```python
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()                      # INSERT into Contact table
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')
```

**Important for class samples:**  
Some samples only `redirect(...)` and **forget** `form.save()`.  
Without `save()`, Admin stays empty. **Always save if you want DB storage.**

---

### Step E — URLs (`api/urls.py`)

```python
path('contact/', views.contact, name='contact'),
path('contact/success/', views.contact_success, name='contact_success'),
```

`config/urls.py` must still `include('api.urls')`.

---

### Step F — Template (`contact.html`)

Pattern (course-style loop):

```django
<form method="post" action="{% url 'contact' %}">
    {% csrf_token %}

    {% for field in form %}
        <div class="form-group">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}
                <div class="field-errors">{{ field.errors }}</div>
            {% endif %}
        </div>
    {% endfor %}

    <button type="submit">Submit</button>
</form>
```

**Must-haves:**

- `method="post"`
- `{% csrf_token %}` (or you get **403 CSRF**)
- View passes `form` in context

Success page (`contact_success.html`) is a simple thank-you with links home / contact again.

---

### Step G — Admin (`api/admin.py`)

```python
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'created_at')
    search_fields = ('name', 'email', 'contact')
```

View submissions: http://localhost:8081/admin/ → **Contacts**  
(Need `createsuperuser` once.)

---

## 4. Request flow diagram

```text
Browser POST /contact/
        │
        ▼
api/urls.py  →  views.contact
        │
        ▼
ContactForm(request.POST)
        │
   is_valid()? ──no──► re-render contact.html (show errors)
        │ yes
        ▼
form.save()  →  table api_contact (MySQL/SQLite)
        │
        ▼
redirect('contact_success')  →  contact_success.html
```

---

## 5. Manual form vs ModelForm (what we switched from)

| Manual HTML inputs | ModelForm |
|--------------------|-----------|
| You write every `<input name="...">` | Form built from model |
| `request.POST.get('name')` by hand | `form.cleaned_data` / `save()` |
| Easy to mismatch DB columns | Fields stay in sync with model |

We started with a demo form (success message only), then switched to **ModelForm + save** for the graded pattern.

---

## 6. Common midterm mistakes

| Mistake | Result |
|---------|--------|
| Forget `{% csrf_token %}` | 403 CSRF verification failed |
| Forget `form.save()` | Redirect works, DB empty |
| Forget `migrate` | `no such table: api_contact` |
| Forget register in `admin.py` | No Contacts in Admin |
| Wrong `name=` on `redirect` | NoReverseMatch |
| Field name in form ≠ model | Validation / save errors |

---

## 7. Commands cheat sheet (Docker)

```bash
cd ~/djangoFileTTH
git pull origin main

docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Test: http://localhost:8081/contact/  
Admin: http://localhost:8081/admin/

---

## 8. Files to copy-study in the repo

```text
api/models.py          → class Contact
api/forms.py           → class ContactForm
api/views.py           → contact(), contact_success()
api/urls.py            → contact paths
api/admin.py           → ContactAdmin
api/templates/contact.html
api/templates/contact_success.html
api/migrations/0004_contact.py
```

---

## 9. One-sentence summary for oral defense

“We used a **Contact model**, a **ModelForm** bound to it, a view that on POST runs **is_valid** and **save**, then **redirects** to a success page; **csrf_token** protects the form and **Admin** lists the saved rows.”

---

*Use this file to rebuild the same flow on your midterm project.*
