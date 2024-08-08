from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Message
from django.http import HttpResponse, JsonResponse


# Create your views here.
def home(request):
    return render(request, 'home.html')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.filter(name=room).first()
    if room_details is None:
        return redirect('home.html')  # Redirect to home or an error page if room does not exist
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
    })


def checkview(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        username = request.POST['username']

        print(f"Room Name: {room_name}, Username: {username}")

        if Room.objects.filter(name=room_name).exists():
            return redirect(f'/{room_name}/?username={username}')
        else:
            new_room = Room.objects.create(name=room_name)
            new_room.save()
            return redirect(f'/{room_name}/?username={username}')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
