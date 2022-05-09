from http.client import HTTPResponse
from django.shortcuts import render , redirect
from django.http import HttpResponse
import sqlite3
from django.contrib.auth import login , authenticate , logout
from django.contrib import messages

def updateData(request) :
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    try : 
        c.execute("""CREATE TABLE datas (current REAL , voltage REAL , energy REAL)""")
    except :
        print("Table Exists")
    try : 
        voltage = float(request.POST.get('voltage'))
        current = float(request.POST.get('current'))
        print(voltage*current)
        energy = voltage*current
        c.execute(f"""INSERT INTO datas VALUES ({ current } , { voltage } , { energy })""")
        c.execute("SELECT * FROM datas ;")
        values = c.fetchall()
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
    try: 
        conn = sqlite3.connect("Data.db")
        c = conn.cursor()
        c.execute("DROP TABLE datas;")
        conn.commit()
        conn.close()
        return HttpResponse("Deleted")
    except :
        print("Table Doesn't Exist")
        return HttpResponse()

def login(request):
    return 
