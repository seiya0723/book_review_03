from django.urls import path
from . import views

app_name    = "book"
urlpatterns = [
    path('', views.index, name="index"),

    #引数ありのURL。下記の場合 single/3/ であれば、pk=3 が引数としてviews.singleが実行される。single/test/の場合は404
    path("single/<int:pk>", views.single, name="single"),
]
