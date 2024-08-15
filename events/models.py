from django.db import models
from django.contrib.auth.models import User

class SportType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    captain = models.ForeignKey('Player', related_name='captain_of', on_delete=models.SET_NULL, null=True, blank=True)
    vice_captain = models.ForeignKey('Player', related_name='vice_captain_of', on_delete=models.SET_NULL, null=True, blank=True)
    head_coach = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='team_logos/')
    flag = models.ImageField(upload_to='team_flags/')

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    score = models.IntegerField()
    position = models.CharField(max_length=100, default='Unassigned')  # Example default value

    def __str__(self):
        return self.name
    
class Venue(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Event(models.Model):
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    date_time = models.DateTimeField()
    team1 = models.ForeignKey(Team, related_name='team1_events', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_events', on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,default=1)
    betting_price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    winning_team = models.ForeignKey(Team, related_name='won_events', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.team1} vs {self.team2} - {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"


from django.db import models
from django.contrib.auth.models import User

class Bet(models.Model):
    EVENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
    ]
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    predicted_winner = models.ForeignKey('Team', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potential_payout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    odds = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=EVENT_STATUS_CHOICES, default='PENDING')
    # other fields...

    def __str__(self):
        return f"{self.user.username} - {self.event} - {self.amount}"



class Result(models.Model):
    event = models.OneToOneField('Event', on_delete=models.CASCADE)
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    winner = models.ForeignKey('Team', related_name='result_won_events', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event} - Result"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('BET_SETTLEMENT', 'Bet Settlement'),
    ]
    type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount}"

class League(models.Model):
    name = models.CharField(max_length=100)
    sport_type = models.ForeignKey('SportType', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


# class Comment(models.Model):
#     event = models.ForeignKey('Event', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.event}"

# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()

#     def __str__(self):
#         return self.name

# class Subscription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     plan = models.CharField(max_length=100)
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"{self.user.username} - {self.plan}"
