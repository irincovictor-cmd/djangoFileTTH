from django.urls import path
from . import views

"""
URL map — no overlapping paths between the two sites.

LearnHub  (notebook theme, base.html)
  /                     home
  /home/                home (alias)
  /topics/              topic list
  /topics/<id>/         topic detail
  /about/               about
  /contact/             contact form
  /contact/success/     after submit

Portfolio (dark theme, portfolio.html) — everything under /portfolio/
  /portfolio/                 home
  /portfolio/work/            work
  /portfolio/skills/          skills
  /portfolio/about/           about
  /portfolio/contact/         contact form
  /portfolio/contact/success/ after submit
"""

urlpatterns = [
    # ---------- LearnHub ----------
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("topics/", views.topics, name="topics"),
    path("topics/<int:pk>/", views.topic_detail, name="topic_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),

    # ---------- Portfolio (prefix only — no root /work or /skills) ----------
    path("portfolio/", views.portfolio_home, name="portfolio"),
    path("portfolio/work/", views.portfolio_work, name="portfolio_work"),
    path("portfolio/skills/", views.portfolio_skills, name="portfolio_skills"),
    path("portfolio/about/", views.portfolio_about, name="portfolio_about"),
    path("portfolio/contact/", views.portfolio_contact, name="portfolio_contact"),
    path(
        "portfolio/contact/success/",
        views.portfolio_contact_success,
        name="portfolio_contact_success",
    ),
]
