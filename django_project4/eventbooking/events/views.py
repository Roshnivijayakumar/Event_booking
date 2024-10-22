from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Booking
from .forms import BookingForm


# List all available events
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


# Show details for a specific event
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_details.html', {'event': event})


# Handle booking for an event
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats_requested = form.cleaned_data['seats_booked']
            if event.available_seats >= seats_requested:
                # Reduce the available seats in the event
                event.available_seats -= seats_requested
                event.save()

                # Create a booking
                booking = form.save(commit=False)
                booking.user = request.user
                booking.event = event
                booking.save()

                messages.success(request, 'Booking successful!')
                return redirect('event_detail', event_id=event.id)
            else:
                messages.error(request, 'Not enough seats available.')
    else:
        form = BookingForm()

    return render(request, 'events/book_event.html', {'event': event, 'form': form})