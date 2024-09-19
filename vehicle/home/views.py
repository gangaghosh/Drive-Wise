from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os

def home(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def drowsiness(request):
  template = loader.get_template('drowsiness.html')
  return HttpResponse(template.render())

def lane(request):
  template = loader.get_template('lane.html')
  return HttpResponse(template.render())

def traffic(request):
  template = loader.get_template('traffic.html')
  return HttpResponse(template.render())

def pedstrain(request):
  template = loader.get_template('pedstrain.html')
  return HttpResponse(template.render())

def service(request):
  template = loader.get_template('service.html')
  return HttpResponse(template.render())




import subprocess
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

def run_detection_script(request):
    result = subprocess.run(['python', r'driver-fatigue-detection-system-master\drowsiness detection.py'], capture_output=True, text=True)

   
    return HttpResponseRedirect(reverse('drowsiness'))
  


import subprocess
from django.http import HttpResponse

def run_traffic_script(request):
    result = subprocess.run(['python', r'traffic\traffic.py'], capture_output=True, text=True)

    return HttpResponseRedirect(reverse('traffic'))




import subprocess
from django.http import HttpResponse

def run_ped_script(request):
    result = subprocess.run(['python', r'pedstrain\ped.py'], capture_output=True, text=True)

    return HttpResponseRedirect(reverse('pedstrain'))
  
import subprocess
from django.http import HttpResponse

def run_lane_script(request):
    result = subprocess.run(['python', r'lane_detection-master\laneDetection.py'], capture_output=True, text=True)

    return HttpResponseRedirect(reverse('lane'))


# app
from django.shortcuts import render
from django.http import JsonResponse
from .detection import drowsiness_detection
from threading import Thread

def run_script(request, script_name):
    if script_name == 'drowsiness':
        thread = Thread(target=drowsiness_detection)
    # Add other script triggers here
    else:
        return JsonResponse({'status': 'Unknown script'}, status=400)
    
    thread.start()
    return JsonResponse({'status': f'{script_name} detection started'})


# Similar views for other functionalities can be added here
from django.http import JsonResponse

def run_map_script(request):
    # Logic for Google Map Detection goes here.
    
    # For now, let's just return a success message as an example.
    return JsonResponse({'status': 'Google Map Detection started successfully!'})
