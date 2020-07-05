import datetime
from dateutil.parser import parse

def clean_data(data):
    """ Return object with the latest date """
    countries = []
    cleaned_data =[]
    for obj in data:
        if obj["country"] in countries:
            for item in cleaned_data:
                if item["date"] < obj["date"] and item["country"]==obj["country"]:
                    cleaned_data.remove(item)
                    cleaned_data.append(obj)           
        else:
            countries.append(obj["country"])
            cleaned_data.append(obj)
    return cleaned_data

def convert_date(data):
    """ Convert date to dd/mm/yy """
    converted_date = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%fZ")
    return converted_date
