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

# Create your views here.
def hello(request):
    return JsonResponse({"message": "Helloworld"})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def save_data(request):
    """ List data or save data"""
    # alter provided date to dd/mm/yy
    ## save data
    if request.method == 'POST':
        cleaned_data = clean_data(request.data)
        serializer = RawDataSerializer(data=cleaned_data, many=True)
        if serializer.is_valid():
            results = serializer.save()
            return JsonResponse({"data": results},status=201)
        return JsonResponse({"message":"Invalid Data"}, status=400)

class TopTenCountriesProducers(generics.ListAPIView):
    """ Return top ten producers """
    serializer_class = ProducerSerializer
    queryset = Produced.top_ten_produced_countries()

    def get(self, request):
        serializer = ProducerSerializer(data=list(self.get_queryset()),many=True, context={"request":request})
        serializer.is_valid()
        return JsonResponse({"results":serializer.data})
    

class TopFiveCountriesRejected(generics.ListAPIView):
    pass

class TopFiveCountriesLeastPendingUnits(generics.ListAPIView):
    pass

class TotalProducedUnitsByDate(generics.ListAPIView):
    pass
    

# def get_top_ten_countries_produced(request):
#     # countries = Country.objects.all()
#     top_ten_countries = Produced.objects.values("country","units").annotate(total_units=Sum("units")).order_by("total_units")[:10]
#     import pdb; pdb.set_trace()
#     # serializer = ProducerSerializer(top_ten_countries, many=True)
#     return JsonResponse({"countries": json.dumps(top_ten_countries)})


# generic view

# top 10 countries with the highest produced units
# top five days that had the most rejected units
# op 5 countries with the least pending units
# total units produced each day this endpoint should be able to filter according to a date range
