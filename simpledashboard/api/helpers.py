import datetime

def clean_data(data):
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
    # date = validated_data["date"]
    converted_date = datetime.datetime.strptime(data[:-17], '%Y-%m-%d')
    return "%s/%s/%s"%(converted_date.day,converted_date.month,converted_date.year)
