from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Sum

import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, generics
from rest_framework.response import Response
import json

from .models import Country, Produced, Pending, Rejected
from .serializers import CountrySerializer, RawDataSerializer, ProducerSerializer
from .helpers import clean_data

def hello(request):
    return JsonResponse({"message": "Helloworld"})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def save_data(request):
    """ List data or save data"""
    # alter provided date to dd/mm/yy > django rejected the requested format
    ## save data
    if request.method == 'POST':
        cleaned_data = clean_data(request.data)
        serializer = RawDataSerializer(data=cleaned_data, many=True)
        if serializer.is_valid():
            results = serializer.save()
            return JsonResponse({"data": results},status=201)
        return JsonResponse({"message":"Invalid Data"}, status=400)

class TopTenCountriesProducers(generics.ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.top_ten_produced_countries()


class TopFiveCountriesRejected(generics.ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.top_five_rejected_countries()

class TopFiveCountriesLeastPendingUnits(generics.ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.top_five_least_pending_contries()

class TotalProducedUnitsByDate(generics.ListAPIView):
    serializer_class = CountrySerializer

    def  get_queryset(self):

        date_range = [self.request.GET.get("start"), self.request.GET.get("end")]
        queryset = Country.filter_by_date(date_range)
        return queryset
    
