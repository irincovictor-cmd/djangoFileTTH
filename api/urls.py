from django.urls import path
from . import views

"""
URL map — no overlapping paths between the two sites.

LearnHub  (notebook theme)
  /                     home
  /home/                home (alias)
  /topics/              topic list (+ add modal)
  /topics/manage/       POST add / replace / delete topic
  /topics/<id>/         topic detail
  /about/               about
  /contact/             contact form → Contact messages only
  /contact/success/     after submit

Portfolio — under /portfolio/
  /portfolio/contact/   contact form → Profiles only
"""

urlpatterns = [
    # ---------- LearnHub ----------
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("topics/", views.topics, name="topics"),
    path("topics/manage/", views.topic_manage, name="topic_manage"),
    path("topics/<int:pk>/", views.topic_detail, name="topic_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),

    # ---------- Portfolio ----------
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
