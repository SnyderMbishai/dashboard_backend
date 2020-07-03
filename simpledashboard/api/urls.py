from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('raw_data', views.save_data, name='raw_data'),
    path('top_ten_produced', views.TopTenCountriesProducers.as_view(), name="top_produced"),
    path('top_five_rejected', views.TopFiveCountriesRejected.as_view(), name="top_rejected"),
    path('least_five_pending', views.TopFiveCountriesLeastPendingUnits.as_view(), name="least_pending"),
    # path('date_range', views.TotalProducedUnitsByDate.as_view(), name="filtered_by_date"),
]
