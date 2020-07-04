from django.db import models
from django.db.models import Sum

class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @classmethod
    def top_ten_produced_countries(cls):
        """ Return top ten countries with the most produced """
        top_ten_countries = cls.objects.annotate(unit_sum=Sum('producer__units')).values('name','unit_sum').order_by('-unit_sum')[0:10]
        return top_ten_countries
    
    @classmethod
    def top_five_rejected_countries(cls):
        """ Return top five rejected countries """
        top_five_countries = cls.objects.annotate(unit_sum=Sum('rejected__units')).values('name', 'unit_sum').order_by('-unit_sum')[0:5]
        return top_five_countries

    @classmethod
    def top_five_least_pending_contries(cls):
        """ Return least five pending countries """
        least_five_pending_countries = cls.objects.annotate(unit_sum=Sum('pending__units')).values('name','unit_sum').order_by('-unit_sum').reverse()[0:5]
        return least_five_pending_countries

    @classmethod
    def filter_by_date(cls, date_range):
        filtered = cls.objects.filter(producer__date__range=date_range).annotate(total_units=Sum('producer__units'))
        return filtered

class Produced(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="producer")
    units = models.IntegerField()
    date = models.DateTimeField(blank=False)

class Rejected(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    units = models.IntegerField()
    date = models.DateTimeField(blank=False)


class Pending(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    units = models.IntegerField()
    date = models.DateTimeField(blank=False)
