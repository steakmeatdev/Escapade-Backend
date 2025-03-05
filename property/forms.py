from django.forms import ModelForm
from .models import Property, Reservation


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = (
            "title",
            "description",
            "price_per_night",
            "bedrooms",
            "bathrooms",
            "guests",
            "country",
            "country_code",
            "category",
            "image",
        )


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "guests",
            "start_date",
            "end_date",
            "number_of_nights",
            "total_price",
        ]
