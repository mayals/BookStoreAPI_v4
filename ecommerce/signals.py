from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Payment

# @receiver(post_save, sender=Order)
def create_payment(sender, instance, created, **kwargs):
    order = instance
    if created:
        Payment.objects.create(order=order, amount=order.total_amount)
