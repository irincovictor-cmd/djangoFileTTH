from django.urls import path
from . import views

urlpatterns = [
    # Portfolio
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("work/", views.work, name="work"),
    path("skills/", views.skills, name="skills"),
    path("about/", views.about, name="about"),

    # LearnHub
    path("topics/", views.topics, name="topics"),
    path("topics/<int:pk>/", views.topic_detail, name="topic_detail"),

    # Contact → DB + admin
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
]
