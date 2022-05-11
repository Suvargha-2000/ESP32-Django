from asyncio import constants
from http.client import HTTPResponse
from os import execv
from pickle import GLOBAL
from django.shortcuts import render , redirect
from django.http import HttpRequest, HttpResponse
import sqlite3
from django.contrib.auth import login , authenticate , logout
from django.contrib import messages
import time

from datetime import datetime
import pytz

def visualRepresent(request) :
    tz_kol = pytz.timezone('Asia/Calcutta') 
    datetime_kol = datetime.now(tz_kol)

    try:
        energy = []
        times = []
        conn = sqlite3.connect("Data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM datas ;")
        values = c.fetchall()
        x = 0
        
        for i in values : 
            
            energy.append(float(i[2])/1000)
            times.append(i[3])
            x = x + 1
        
    except:
        pass
    return render (request , 'visualization.html' , {"energy" : energy , "times" : times})


def updateData(request) :
    passkey = "EnergyMeterProject"

    if request.POST.get('passkey') != passkey :
        print(request.POST.get('passkey'))
        return HttpResponse("Passkey Doesn't Match")

    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    try : 
        c.execute("""CREATE TABLE datas (current REAL , voltage REAL , energy REAL , time REAL)""")
    except :
        print("Table Exists")
    try : 
        voltage = float(request.POST.get('voltage'))
        current = float(request.POST.get('current'))
        print(voltage*current)
        energy = voltage*current

        tz_kol = pytz.timezone('Asia/Calcutta') 
        datetime_kol = datetime.now(tz_kol)
        
        time_INT = int(datetime_kol.strftime("%H%M%S"))
        # named_tuple = time.localtime()
        # time_INT = int(time.strftime("%H%M%S", named_tuple))
        c.execute(f"""INSERT INTO datas VALUES({ current },{ voltage },{ energy },{time_INT})""")
        conn.commit()
        conn.close()
        return HttpResponse(request.POST)
    except : 
        return HttpResponse("Cancelled")
        print("Value Error")


def home(request):
    conn = sqlite3.connect("Data.db")
    try : 
        c = conn.cursor()
        c.execute("SELECT * FROM datas ;")
        values = c.fetchall()
        energy = 0.0
        for i in values : 
            energy = energy + i[2]
        energy = round((energy / 1000) , 5)
        conn.commit()
        conn.close()
        return render(request , 'home.html' , {"energy" : energy , "voltage" : values[-1][1] , "current" : values[-1][0]} )
    except :
        return render(request , 'home.html' , {"data" : "Not Available"})


def deleteDB(request):
    if request.method == "POST" :
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try :
                    conn = sqlite3.connect("Data.db")
                    c = conn.cursor()
                    c.execute("DROP TABLE datas;")
                    conn.commit()
                    conn.close()
                    return redirect(home)
                except:
                    return redirect(home)
            else:
                return redirect('delete')

    else : 
        return render(request , 'deleteDBform.html') 
