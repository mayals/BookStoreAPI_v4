from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, Book




@receiver([post_save, post_delete], sender=Review)
def update_Book_stats(sender, instance, **kwargs):
    
    book = instance.book
    book_reviews = Review.objects.filter(book=book)

    book_reviews_count = book_reviews.count()
    # Get the average rating if there are at least 1 rating else return the default rating
    if book_reviews_count != 0:
        book.average_rating = book_reviews.aggregate(avg_rating=Avg('rating_value'))['avg_rating']
    else:
        book.average_rating = Book._meta.get_field("average_rating").get_default()
    book.save()

