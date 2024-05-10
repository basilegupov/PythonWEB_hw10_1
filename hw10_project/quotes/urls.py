from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name ="root"),
    path("<int:page>", views.main, name ="root_paginate"),
    path('author/<str:author_id>', views.author_about, name='author'),
    path('tag/<str:tag_name>/', views.tag_page, name='tag_page'),
    path('author_for_tag/<int:author_id>', views.author_for_tag, name='author_for_tag'),
    path('top-tags/', views.render_tags, name='top_tags'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('add_tag/', views.add_tag, name='add_tag'),
]
