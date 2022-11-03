from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import CreateRoomForm
from .models import Room, Message


@login_required
def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            Room.objects.create(name=form.cleaned_data['name'])
        rooms = Room.objects.all()
        return render(request, 'APP_Room/rooms.html', {'rooms': rooms,
                                                       'form': form})


@login_required
def rooms(request):
    rooms = Room.objects.all()
    form = CreateRoomForm()
    return render(request, 'APP_Room/rooms.html', {'rooms': rooms,
                                                   'form': form})


@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    # Revers for get last 50msgs (no first)
    # and revers again for right ordering
    messages = Message.objects.filter(
        room=room).reverse()[0:settings.PAGINATION_MSGS_LIMIT][::-1]
    print(messages)
    return render(request, 'APP_Room/room.html', {'room': room, 'messages': messages})
