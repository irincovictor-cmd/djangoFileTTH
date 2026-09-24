from django.urls import path
from . import views

urlpatterns = [
    # ---------- LearnHub (notebook theme) ----------
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("topics/", views.topics, name="topics"),
    path("topics/<int:pk>/", views.topic_detail, name="topic_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),

    # ---------- Portfolio (dark theme) — own namespace ----------
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

    # Legacy short URLs → portfolio (so old links still work)
    path("work/", views.portfolio_work, name="work"),
    path("skills/", views.portfolio_skills, name="skills"),
]
