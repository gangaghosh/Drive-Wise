from django.urls import path
from . import views
from playsound import playsound

urlpatterns = [
    path('', views.home, name='home'),
       path('drowsiness/', views.drowsiness, name='drowsiness'),
        path('lane/', views.lane, name='lane'),
        path('traffic/', views.traffic, name='traffic'),
        path('pedstrain/', views.pedstrain, name='pedstrain'),
        path('service/', views.service, name='service'),
        
        
        # path('driver/', views.start_detection, name='start_detection'),
       

    path('run-detection-script/', views.run_detection_script, name='run_detection_script'),


         path('run-ped-script/', views.run_ped_script, name='run_ped_script'),
         
          path('run-traffic-script/', views.run_traffic_script, name='run_traffic_script'),
          
          path('run-lane-script/', views.run_lane_script, name='run_lane_script'),
        
        
          path('run_script/<str:script_name>/', views.run_script, name='run_script'),
          
         
        
        
        
       

    path('run_map_script/', views.run_map_script, name='run_map_script'),


        
]