from django.urls import path
from django.contrib.auth import views as auth_views

from .views import IndexView, BookRegisterView, BookAllView, BookUpdateView

# {% url 'blog:post-list' %}
app_name = 'book'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('book-register', BookRegisterView.as_view(), name='book-register'),
    path('book-all', BookAllView.as_view(), name='book-all'),
    path('book-update/<int:pk>', BookUpdateView.as_view(), name='book-update'),
    # Default Django directory responsible for logging out the page and redirecting to the login page.
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
]
