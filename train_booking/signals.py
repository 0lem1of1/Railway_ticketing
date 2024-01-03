# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Wallet

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        print(f"Wallet created for user: {instance.username}")
        Wallet.objects.create(user=instance)
    else:
        print(f"User {instance.username} updated, wallet not created")
