from django import forms
from .models import RoomBooking, TableReservation


class RoomBookingForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = RoomBooking
        fields = ('check_in', 'check_out', 'guests', 'special_requests')
        widgets = {
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests?'}),
        }


class TableReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = TableReservation
        fields = ('date', 'time', 'guests', 'occasion', 'special_requests')
        widgets = {
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'occasion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Birthday, Anniversary, etc.'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
