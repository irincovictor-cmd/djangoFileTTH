from django.urls import path
from . import views

urlpatterns = [
    # Portfolio / home
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("portfolio/", views.portfolio, name="portfolio"),

    # LearnHub pages (kept)
    path("topics/", views.topics, name="topics"),
    path("topics/<int:pk>/", views.topic_detail, name="topic_detail"),
    path("about/", views.about, name="about"),

    # Contact → database + admin
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
]
