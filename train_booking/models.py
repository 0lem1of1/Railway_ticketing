from django.db import models
from django.core.exceptions import ValidationError
from user_app.models import User
from datetime import timedelta,timezone,datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _




from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime

class Train(models.Model):
    MONDAY = 'Mon'
    TUESDAY = 'Tue'
    WEDNESDAY = 'Wed'
    THURSDAY = 'Thu'
    FRIDAY = 'Fri'
    SATURDAY = 'Sat'
    SUNDAY = 'Sun'

    DAYS_OF_WEEK_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    name = models.CharField(max_length=100)
    source_station = models.CharField(max_length=100)
    destination_station = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    days_of_the_week = models.CharField(max_length=50, help_text="Comma-separated list of days", blank=True) #Change this to a ArrayField after switching to postgre database
    total_seats = models.PositiveIntegerField()
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)  # Added is_active field



    def __str__(self):
        return self.name

    def clean(self):
        if self.departure_time >= self.arrival_time:
            raise ValidationError("Departure time must be before arrival time.")

        if self.total_seats < 0:
            raise ValidationError("Total seats must be a non-negative value.")

        if self.fare < 0:
            raise ValidationError("Fare must be a non-negative value.")

    @classmethod
    def search_trains(cls, source_station, destination_station, departure_time):
        current_date = timezone.now().date()
        # Perform a query to filter trains based on search criteria
        queryset = cls.objects.filter(
            source_station__icontains=source_station,
            destination_station__icontains=destination_station,
            departure_time__gte=departure_time,
            is_active=True,  # Make sure to filter active trains
        )
        return queryset

    def create_journeys_for_next_months(self, num_months=4):
        # Ensure days_list is a list
        if isinstance(self.days_of_the_week, str):
            days_list_strings = self.days_of_the_week.split(',') if self.days_of_the_week else []
            cleaned_days_list = [day.strip("[] '") for string in days_list_strings for day in string.split(",")]
        elif isinstance(self.days_of_the_week, list):
            cleaned_days_list = [day.strip("[] '") for day in self.days_of_the_week]
        else:
            cleaned_days_list = []

        current_date = datetime.today().date()
        existing_journeys = Journey.objects.filter(train=self)

        for i in range(num_months * 30):
            departure_date = current_date + timedelta(days=i)

            
            # Check if the current day matches any day in the 'cleaned_days_list' field
            if departure_date.strftime("%a") in cleaned_days_list:
                # Check if a journey with the same attributes already exists
                existing_journey = existing_journeys.filter(departure_date=departure_date)
                if not existing_journey.exists():
                    arrival_date = departure_date + timedelta(days=1)

                    Journey.objects.create(
                        train=self,
                        departure_date=departure_date,
                        arrival_date=arrival_date,
                    )

class Journey(models.Model):
    departure_date = models.DateField()
    train = models.ForeignKey(Train, on_delete=models.CASCADE, null=False)
    arrival_date = models.DateField()

    def __str__(self):
        return f"{self.train.name} /// {self.train.source_station} - {self.train.destination_station} - {self.departure_date}"

    class Meta:
        verbose_name_plural = "Journeys"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=None)
    is_cancelled = models.BooleanField(default=False)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.journey.train.name} - {self.journey.departure_date}"

    def check_seat_availability(self):
        # Get the total capacity of the train
        total_capacity = self.journey.train.total_seats

        # Get the number of booked seats for the journey date
        booked_seats = Booking.objects.filter(journey=self.journey).count()

        # Check if there are enough available seats
        available_seats = total_capacity - booked_seats
        return available_seats >= self.passengers.count()

class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        if self.gender:
            return f"{self.name} ({self.get_gender_display()}), Age: {self.age}"
        else:
            return f"{self.name}, Age: {self.age}"

    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"
    
    def add_money(self,amount):
        self.balance += amount
        return True
    def subtract_money(self, amount):
        if amount > self.balance:
            raise ValueError("The amount to be subtracted exceeds the current balance.")
        self.balance -= amount        
        return True

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_wallet(sender, instance, **kwargs):
    instance.wallet.save()