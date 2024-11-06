from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=122, verbose_name=_("name"))


class Book(BaseModel):
    title = models.CharField(max_length=122, verbose_name=_("title"))
    description = models.TextField(max_length=122, verbose_name=_("description"))
    pdf = models.FileField(upload_to="book/", verbose_name=_("File"))
    rating = models.IntegerField(verbose_name=_("rating"), default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.TextField(max_length=250)
    rating = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")


class MyFavoriteBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("book"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))


class Author(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("book"))
    about = models.TextField(max_length=250, verbose_name=_("About"))


class Publisher(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("book"))
    about = models.TextField(verbose_name=_("about"))


# class ReadingList(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
#


class BookShelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("book"))
    

