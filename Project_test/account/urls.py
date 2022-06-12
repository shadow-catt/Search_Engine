# Programmer: Jack
# Student ID: 1930026143
# Date: 2020/1/24
# Requirements:

from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("Home", views.book_search, name='book_search'),
    path("book-list", views.book_list, name='book_list'),
    path("books_details", views.book_detail, name='book_detail')
]