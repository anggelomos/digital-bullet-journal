import requests
from datetime import date

class  DataRetriever:
    def __init__(self, rescuetime_key):
        self.rescuetime_key = rescuetime_key

    current_date = str(date.today())

    def productivity_time(self, date: str=current_date)->dict:
        """Capture data from the rescuetime productivity categories (very productive, productive, neutral, distracting, very distracting, total) using the rescuetime API.

        Parameters
        ----------
        date : str, optional
            Date from which the data should be taken in Format ISO 8601 "YYYY-MM-DD", Ex. 2020-08.10 by default current_date

        Returns
        -------
        productivity_time: dict
            Dictionary where the key is a productivity categories (very productive, productive, neutral, distracting, very distracting, total) and the value is the time in seconds, Ex {'very productive': 8432, 'productive': 722, 'neutral': 1843, 'distracting': 970, 'very distracting': 23, 'total': 11990}.  
        """
        raw_data = requests.get(f"https://www.rescuetime.com/anapi/data?key={self.rescuetime_key}&perspective=interval&restrict_kind=productivity&interval=day&restrict_begin={date}&restrict_end={date}&format=json")
        raw_productivity_data = raw_data.json()["rows"]
        productivity_time = {"very productive":0, "productive": 0, "neutral": 0, "distracting": 0, "very distracting": 0, "total":0}
        for data in raw_productivity_data:
            category = data[3]
            time = data[1]
            if category == 2:
                productivity_time["very productive"] = round(time/3600, 2)
            elif category == 1:
                productivity_time["productive"] = round(time/3600, 2)
            elif category == 0:
                productivity_time["neutral"] = round(time/3600, 2)
            elif category == -1:
                productivity_time["distracting"] = round(time/3600, 2)
            elif category == -2:
                productivity_time["very distracting"] = round(time/3600, 2)
            else:
                raise IndexError("Wrong productivity category")
            productivity_time["total"] += time
        return productivity_time
