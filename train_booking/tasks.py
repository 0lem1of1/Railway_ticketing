# tasks.py
from celery import shared_task
from .models import Train

@shared_task
def create_journeys_for_next_months():
    for train in Train.objects.all():
        train.create_journeys_for_next_months()
