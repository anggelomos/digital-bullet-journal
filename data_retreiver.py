import requests

raw_data = requests.get('https://www.rescuetime.com/anapi/data?key=B63SG1dvEUH_h5YZAus3mZLlTzKUyvlt5_KBmyhZ&perspective=interval&restrict_kind=productivity&interval=day&restrict_begin=2020-08-01&restrict_end=2020-08-01&format=json')
raw_productivity_data = raw_data.json()["rows"]
productivity_time = {"very productive":0, "productive": 0, "neutral": 0, "distracting": 0, "very distracting": 0}
for data in raw_productivity_data:
    category = data[3]
    time = data[1]
    if category == 2:
        productivity_time["very productive"] = time
    elif category == 1:
        productivity_time["productive"] = time
    elif category == 0:
        productivity_time["neutral"] = time
    elif category == -1:
        productivity_time["distracting"] = time
    elif category == -2:
        productivity_time["very distracting"] = time
    else:
        raise IndexError("Wrong productivity category")

print(productivity_time)