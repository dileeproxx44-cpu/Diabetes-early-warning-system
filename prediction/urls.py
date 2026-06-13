from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_view, name='predict'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('api/patients/',patients_api,name='patients_api'),
    path('api/predictions/', views.predictions_api),
    path('api/alerts/', views.alerts_api),
    path('api/predict/', views.predict_api),
    path('history/',views.history_view,name='history'),
    path('profile/',views.profile_view,name='profile'),
    path('export-csv/',views.export_csv,name='export_csv'),
]