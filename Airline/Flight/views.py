from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
	context={
		"Flights": Flight.objects.all()
	}
	return render(request, "Flight/index.html", context)

def flight(request, flight_id):
	try:
		flight=Flight.objects.get(pk=flight_id)
	except Flight.DoesNotExist:
		raise Http404("flight does not exist.")	
	
	context = {
		"flight": flight,
		"passengers": flight.passengers.all(),
		"non_passengers": Passenger.objects.exclude(flights=flight).all()
	}
	return render (request, "Flight/flight.html", context)	
def book(request, flight_id):
	try:
		passenger_id = int(request.POST["passenger"])
		passenger = Passenger.objects.get(pk = passenger_id)
		flight = Flight.objects.get(pk = flight_id)
	except Passenger.DoesNotExist:
		return render(request, "Flight/error.html", {"message": "NO passenger."})
	except Flight.DoesNotExist:
		return render(request, "Flight/error.html", {"message": "NO flights."})	
	except KeyError:
		return render(request, "Flight/error.html", {"message": "NO selection."})

	passenger.flights.add(flight)
	return HttpResponseRedirect(reverse("flight" , args=(flight_id,)))