from django.db import models
from django.db.models import Sum

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Produced(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="producer")
    units = models.IntegerField()
    date = models.CharField(max_length=200)

    @classmethod
    def top_ten_produced_countries(cls):
        top_ten_countries = cls.objects.values("country","units").annotate(total_units=Sum("units")).order_by('-total_units')[0:10]
        import pdb; pdb.set_trace()
        return top_ten_countries

    def filter_by_date(self, date_range):
        pass

class Rejected(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    units = models.IntegerField()
    date = models.CharField(max_length=200)

    def top_five_rejected_countries(self):
        pass

class Pending(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    units = models.IntegerField()
    date = models.CharField(max_length=200)

    def top_five_least_pending_contries(self):
        pass