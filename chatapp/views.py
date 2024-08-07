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
        return redirect('home')  # Redirect to home or an error page if room does not exist
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    room_details, created = Room.objects.get_or_create(name=room)
    return redirect(f'/{room}/?username={username}')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    room = get_object_or_404(Room, id=room_id)
    new_message = Message.objects.create(value=message, user=username, room=room)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    try:
        room_details = get_object_or_404(Room, name=room)
        messages = Message.objects.filter(room=room_details)
        message_list = [{"user": msg.user, "value": msg.value, "date": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for
                        msg in messages]
        return JsonResponse({"messages": message_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
