from django.shortcuts import render, HttpResponse
from events.models import Event, SportType
# Create your views here.


def index(request):
    events = Event.objects.all()
    context = {
        'events': events
    }

    return render(request, 'usersite/index.html', context)

def detail_of_event(request, id):
    events = Event.objects.get(id=id)
    context = {
        'events': events
    }

    return render(request, 'usersite/details_of_event.html', context)



def about_us(request):
    return render(request, 'usersite/about.html')

def contact_us(request):
    return render(request, 'usersite/contact.html')

def all_events(request):
    cricket_sport_type = SportType.objects.get(name="Cricket")
    footbal_sport_type = SportType.objects.get(name="Football")
    basebal_sport_type = SportType.objects.get(name="Baseball")
    vollybal_sport_type = SportType.objects.get(name="Vollyball")

    circketevents = Event.objects.filter(sport_type=cricket_sport_type)
    footbalevents = Event.objects.filter(sport_type=footbal_sport_type)
    basebalevents = Event.objects.filter(sport_type=basebal_sport_type)
    vollybalevents = Event.objects.filter(sport_type=vollybal_sport_type)

    context = {
        'cricketevents': circketevents,
        'footbalevents':footbalevents,
        'basebalevents':basebalevents,
        'vollybalevents':vollybalevents,
    }
    return render(request, 'usersite/allevents.html', context)


# def showallevents(request):
#     cricket_sport_type = SportType.objects.get(name="Cricket")
#     circketevents = Event.objects.filter(sport_type=cricket_sport_type)
#     context = {
#         'cricketevents': circketevents,
#     }
#     return render(request, 'usersite/testt.html', context)


