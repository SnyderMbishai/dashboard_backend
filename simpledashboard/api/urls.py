from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('raw_data', views.save_data, name='raw_data'),
    path('top', views.TopTenCountriesProducers.as_view(), name="top_ten"),
]
