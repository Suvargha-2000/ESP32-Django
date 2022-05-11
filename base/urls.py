from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name="home"),
    path('update/' , views.updateData , name="updatedata"),
    path('deleteDB/' , views.deleteDB , name="delete"),
    path('visualization/' , views.visualRepresent , name="visual")
    # path('deleteDBform/' , views.DeleteDBform)
]
