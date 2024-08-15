from django import forms
from .models import SportType, Team, Player, Event, Bet, Result, Transaction, League, Venue

class SportTypeForm(forms.ModelForm):
    class Meta:
        model = SportType
        fields = ['name']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'captain', 'head_coach', 'logo', 'flag']

    
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['captain'].queryset = Player.objects.filter(team=self.instance)
        else:
            self.fields['captain'].queryset = Player.objects.all()


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'age', 'team', 'score', 'position']
        
class BulkPlayerForm(forms.Form):
    players_data = forms.CharField(widget=forms.Textarea, help_text="Enter player details in the format: name, age, score, position, one per line.")



class EventForm(forms.ModelForm):
    date_time = forms.DateTimeField(widget=forms.TextInput(attrs={
        'type': 'datetime-local'
    }))
    
    class Meta:
        model = Event
        fields = ['name','sport_type', 'date_time', 'team1', 'team2', 'venue', 'betting_price', 'short_description', 'long_description']


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['event', 'user', 'predicted_winner']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['event', 'team1_score', 'team2_score', 'winner']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user', 'type', 'amount']

class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'sport_type', 'start_date', 'end_date']

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'city', 'country', 'capacity']


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['event', 'user', 'predicted_winner', 'amount', 'potential_payout', 'odds', 'status']

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'city', 'country', 'capacity']
        
class BulkVenueForm(forms.Form):
    venues_data = forms.CharField(widget=forms.Textarea, help_text="Enter one venue per line in the format: name, city, country, capacity")

