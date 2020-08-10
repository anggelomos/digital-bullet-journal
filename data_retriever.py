import requests
from datetime import date

class  DataRetriever:
    def __init__(self, rescuetime_key):
        self.rescuetime_key = rescuetime_key

    current_date = str(date.today())

    def productivity_time(self, date: str=current_date):
        raw_data = requests.get(f"https://www.rescuetime.com/anapi/data?key={self.rescuetime_key}&perspective=interval&restrict_kind=productivity&interval=day&restrict_begin={date}&restrict_end={date}&format=json")
        raw_productivity_data = raw_data.json()["rows"]
        productivity_time = {"very productive":0, "productive": 0, "neutral": 0, "distracting": 0, "very distracting": 0, "total":0}
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
            productivity_time["total"] += time
        return productivity_time
