# main/forms.py
from django import forms
from .models import Train, Booking, Journey, Passenger,Station
from django.forms import inlineformset_factory


class JourneySearchForm(forms.Form):
    source_station = forms.CharField(label='Source Station', max_length=100)
    destination_station = forms.CharField(label='Destination Station', max_length=100)
    departure_date = forms.DateField(label='Departure Date', widget=forms.DateInput(attrs={'type': 'date'}))

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name']

class AddTrainForm(forms.ModelForm):
    days_of_the_week = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        help_text="Select the days of the week for the train service.",
    )

    route_input = forms.CharField(
        label="Route",
        help_text="Enter the route as a comma-separated list of stations.",
    )

    class Meta:
        model = Train
        exclude = ['source_station', 'destination_station','route'] 

        widgets = {
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'type': 'time'}),
            'total_seats': forms.NumberInput(attrs={'type': 'number'}),
            'fare': forms.NumberInput(attrs={'type': 'number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['days_of_the_week'].choices = Train.DAYS_OF_WEEK_CHOICES

    def clean_route_input(self):
        route_input = self.cleaned_data['route_input']

        # Split the input into a list of stations
        stations = [station.strip() for station in route_input.split(',')]

        # Check if there are at least two stations
        if len(stations) < 2:
            raise forms.ValidationError("Route must have at least two stations.")

        # Set the source and destination stations
        self.cleaned_data['source_station'] = stations[0]
        self.cleaned_data['destination_station'] = stations[-1]

        return route_input

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender']


PassengerFormSet = inlineformset_factory(Booking, Passenger, form=PassengerForm, extra=1, can_delete=True)


class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(label='Amount', min_value=0.01)


class TrainUpdateForm(forms.ModelForm):
    days_of_the_week = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        help_text="Select the days of the week for the train service. ")

    class Meta:
        model = Train
        fields = '__all__'

        widgets = {
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'type': 'time'}),
            'total_seats': forms.NumberInput(attrs={'type': 'number'}),
            'fare': forms.NumberInput(attrs={'type': 'number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['days_of_the_week'].choices = Train.DAYS_OF_WEEK_CHOICES

        # Show the initial values of the days_of_the_week
        instance = getattr(self, 'instance', None)
        if instance and instance.days_of_the_week:
            self.fields['days_of_the_week'].initial = instance.days_of_the_week.split(',')
            self.fields['days_of_the_week'].help_text += f" Currently selected: {instance.days_of_the_week}"

