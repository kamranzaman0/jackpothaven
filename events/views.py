from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import SportType, Team, Player, Event, Bet, Venue
from .forms import SportTypeForm, TeamForm, BulkPlayerForm, PlayerForm, EventForm, BetForm, VenueForm, BulkVenueForm
from django.contrib import messages

def handle_form(request, form, template_name, redirect_url, context=None):
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    if context is None:
        context = {}
    context['form'] = form
    return render(request, template_name, context)


# SportType Views
def sporttype_list(request):
    sporttypes = SportType.objects.all()
    return render(request, 'events/sports/sportstype_list.html', {'sporttypes': sporttypes})

def sporttype_create(request):
    if request.method == 'POST':
        form = SportTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sporttype_list')
    else:
        form = SportTypeForm()
    return render(request, 'events/sports/sporttype_form.html', {'form': form, 'title': 'Create SportType'})

def sporttype_update(request, pk):
    sporttype = get_object_or_404(SportType, pk=pk)
    if request.method == 'POST':
        form = SportTypeForm(request.POST, instance=sporttype)
        if form.is_valid():
            form.save()
            return redirect('sporttype_list')
    else:
        form = SportTypeForm(instance=sporttype)
    return render(request, 'events/sports/sporttype_form.html', {'form': form, 'title': 'Update SportType'})

def sporttype_delete(request, pk):
    sporttype = get_object_or_404(SportType, pk=pk)
    if request.method == 'POST':
        sporttype.delete()
        return redirect('sporttype_list')
    return render(request, 'events/sports/sporttype_confirm_delete.html', {'sporttype': sporttype})


# Team Views
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'events/teams/team_list.html', {'teams': teams})

def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the Team instance
            return redirect('team_list')  # Redirect to the team list page
    else:
        form = TeamForm()
    return render(request, 'events/teams/team_form.html', {'form': form, 'title': 'Create Team'})
    # return HttpResponse("ok")

def team_update(request, pk):
    team = get_object_or_404(Team, pk=pk)
    form = TeamForm(request.POST or None, request.FILES or None, instance=team)
    return handle_form(request, form, 'events/teams/team_form.html', 'team_list', {'title': 'Update Team'})

def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        team.delete()
        return redirect('team_list')
    return render(request, 'events/teams/team_confirm_delete.html', {'team': team})

# Player Views
def player_list(request):
    players = Player.objects.all()
    return render(request, 'events/players/player_list.html', {'players': players})

def bulk_add_players(request):
    if request.method == 'POST':
        form = BulkPlayerForm(request.POST)
        if form.is_valid():
            players_data = form.cleaned_data['players_data']
            team = Team.objects.get(name="Aus")  # Replace with appropriate logic to get the team
            player_list = []
            for line in players_data.split('\n'):
                details = [detail.strip() for detail in line.split(',')]
                if len(details) == 4:
                    name, age, score, position = details
                    player_list.append(Player(name=name, age=int(age), score=int(score), position=position, team=team))
                else:
                    messages.error(request, "Each line must contain exactly 4 fields: name, age, score, position")
                    return render(request, 'players/bulk_add_players.html', {'form': form})
            Player.objects.bulk_create(player_list)
            messages.success(request, "Players added successfully!")
            return redirect('player_list')
    else:
        form = BulkPlayerForm()
    return render(request, 'events/players/bulk_add_players.html', {'form': form})

def player_create(request):
    form = PlayerForm(request.POST or None)
    return handle_form(request, form, 'events/players/player_form.html', 'player_list', {'title': 'Create Player'})

def player_update(request, pk):
    player = get_object_or_404(Player, pk=pk)
    form = PlayerForm(request.POST or None, instance=player)
    return handle_form(request, form, 'events/players/player_form.html', 'player_list', {'title': 'Update Player'})

def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST':
        player.delete()
        return redirect('player_list')
    return render(request, 'events/players/player_confirm_delete.html', {'player': player})

# Event Views
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    return handle_form(request, form, 'events/event_form.html', 'event_list', {'title': 'Create Event'})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    return handle_form(request, form, 'events/event_form.html', 'event_list', {'title': 'Update Event'})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

# Bet Views
def bet_list(request):
    bets = Bet.objects.all()
    return render(request, 'events/bet/bet_list.html', {'bets': bets})

def bet_create(request):
    form = BetForm(request.POST or None)
    return handle_form(request, form, 'events/bet/bet_form.html', 'adminsite:bet_list', {'title': 'Create Bet'})



def bet_update(request, pk):
    bet = get_object_or_404(Bet, pk=pk)
    form = BetForm(request.POST or None, instance=bet)
    return handle_form(request, form, 'events/bet/bet_form.html', 'adminsite:bet_list', {'title': 'Update Bet'})

def bet_delete(request, pk):
    bet = get_object_or_404(Bet, pk=pk)
    if request.method == 'POST':
        bet.delete()
        return redirect('adminsite:bet_list')
    return render(request, 'events/bet/bet_confirm_delete.html', {'bet': bet})

# Venues Views
def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'events/venue/venue_list.html', {'venues': venues})

def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    return render(request, 'events/venue/venue_detail.html', {'venue': venue})

def venue_create(request):
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('venue_list')
    else:
        form = VenueForm()
    return render(request, 'events/venue/venue_form.html', {'form': form})

def venue_update(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == "POST":
        form = VenueForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('venue_list')
    else:
        form = VenueForm(instance=venue)
    return render(request, 'events/venue/venue_form.html', {'form': form})

def venue_delete(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == "POST":
        venue.delete()
        return redirect('venue_list')
    return render(request, 'events/venue/venue_confirm_delete.html', {'venue': venue})

def bulk_add_venues(request):
    if request.method == 'POST':
        form = BulkVenueForm(request.POST)
        if form.is_valid():
            venues_data = form.cleaned_data['venues_data']
            venue_list = []
            for line in venues_data.split('\n'):
                details = [detail.strip() for detail in line.split(',')]
                if len(details) == 4:
                    name, city, country, capacity = details
                    try:
                        capacity = int(capacity)
                        venue_list.append(Venue(name=name, city=city, country=country, capacity=capacity))
                    except ValueError:
                        messages.error(request, f"Invalid capacity value: {capacity}")
                        return render(request, 'events/venue//bulk_add_venues.html', {'form': form})
                else:
                    messages.error(request, "Each line must contain exactly 4 fields: name, city, country, capacity")
                    return render(request, 'events/venue/bulk_add_venues.html', {'form': form})
            Venue.objects.bulk_create(venue_list)
            messages.success(request, "Venues added successfully!")
            return redirect('venue_list')
    else:
        form = BulkVenueForm()
    return render(request, 'events/venue/bulk_add_venues.html', {'form': form})
