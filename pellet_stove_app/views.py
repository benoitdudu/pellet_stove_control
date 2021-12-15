from django.shortcuts import render
from .models import PelletStoveCmd

c = PelletStoveCmd()

def home(request):
    print('request.POST')
    if request.POST:
        c.send_commands = True  if ('send_commands' in request.POST) else False
        c.fan1_speed = request.POST['fan1_speed']
        c.fan2_speed = request.POST['fan2_speed']
        c.flame_power = request.POST['flame_power']
        c.mode = True  if ('mode' in request.POST) else False
        c.SendCommand()

    context = {'pellet_cmds': c,}
    return render(request, 'pellet_stove_app/home.html', context)
