from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg

from apps.common.models import Comment


@receiver(post_save, sender=Comment)
def update_book_rating(sender, instance, **kwargs):
    book = instance.book
    book.rating = book.comments.aggregate(Avg)
    book.save()
