from django.shortcuts import render
from .models import robo
#from django.http import HttpResponse


def home(request):
    #return HttpResponse('home page skill')
    if request.method == 'GET':
        #mydata = robo(Robot=E1,Value=E1data)
        #E2=request.GET.get('E2')
        #E3=request.GET.get('E3')
        #print(E1)
        database = robo.objects.all()
        emergency =robo.objects.filter(Type = "E")
        emergency_queue =robo.objects.filter(Type = "EQ")
        cabin1 =robo.objects.filter(Type = "cabin1")
        cabin2 =robo.objects.filter(Type = "cabin2")
        OT1 =robo.objects.filter(Type = "ot1")
        OT2 =robo.objects.filter(Type = "ot2")
        
        
        
        
        #mydata.save()   
    return render(request,'index.html',
                  context = {"database":database,
                             "emergency":emergency,
                             "emergency_queue": emergency_queue,
                             "cabin1":cabin1,
                             "cabin2":cabin2,
                             "OT1":OT1,
                             "OT2":OT2,
                             
                             
                             })

def contact(request):
    if request.method == 'GET':
        #mydata = robo(Robot=E1,Value=E1data)
        #E2=request.GET.get('E2')
        #E3=request.GET.get('E3')
        #print(E1)
        database = robo.objects.all()
        emergency =robo.objects.filter(Type = "E")
        emergency_queue =robo.objects.filter(Type = "EQ")
        cabin1 =robo.objects.filter(Type = "cabin1")
        cabin2 =robo.objects.filter(Type = "cabin2")
        OT1 =robo.objects.filter(Type = "ot1")
        OT2 =robo.objects.filter(Type = "ot2")
        
        
    return render(request,'contact.html',
                  context = {"database":database,
                             "emergency":emergency,
                             "emergency_queue": emergency_queue,
                             "cabin1":cabin1,
                             "cabin2":cabin2,
                             "OT1":OT1,
                             "OT2":OT2,
                             
                             
                             })