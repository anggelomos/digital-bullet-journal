import datetime
from openpyxl.utils.cell import get_column_letter
from sheets_manager import SheetsManager
from sheets_manager import DatabaseSheet
from sheets_manager import PlotSheet
from data_retriever import DataRetriever

current_date = datetime.date.today()

data_source = DataRetriever(rescuetime_key="B63SG1dvEUH_h5YZAus3mZLlTzKUyvlt5_KBmyhZ")
bullet_database = DatabaseSheet(gsheet_id="1FPia0C2I4pDW-Z5_RlNhR3h2UBY4K4BF26RlHD0J9D8")
plot_sheet = PlotSheet(gsheet_id="1nJpbS-9Z2AMsLFO9rVFWSm8eINcw-khokDQLoZ9oNTI")

def update_database(database_object, data_source, day=None):
    df = database_object.dataframe

    database_data = []
    for index, label in enumerate(list(df.index)):
        database_data.append([])
        try:
            label = label.replace(" time", "")
        except:
            pass
        if day is not None:
            if label is None:
                database_data[index].append("")
                continue
            if day > datetime.date(2020,8,9):
                working_date = day
                productivity_data = data_source.productivity_time(working_date.strftime('%Y-%m-%d'))       
                if label == "logged":
                    database_data[index].insert(0,round(productivity_data["total"], 2))
                else:
                    database_data[index].insert(0,round(productivity_data[label], 2))
                working_date = working_date - datetime.timedelta(1)
        else:
            working_date = current_date
            while df[working_date.strftime('%m-%d')]["logged time"] == None:
                if label is None or label == "":
                    database_data[index].append("")
                else:
                    productivity_data = data_source.productivity_time(working_date.strftime('%Y-%m-%d'))       
                    if label == "logged":
                        database_data[index].insert(0,productivity_data["total"])
                    else:
                        database_data[index].insert(0,productivity_data[label])
                working_date = working_date - datetime.timedelta(1)
                if working_date == datetime.date(2020,8,9):
                    break
    
    for label, index in bullet_database.headers:
        if label not in ["month", "week", "day", "date"]:
            cell_index = index
            break

    working_date = working_date + datetime.timedelta(1)
    insert_cell = bullet_database.date_column(working_date.strftime('%Y-%m-%d')) + str(cell_index)
    bullet_database.write(insert_cell,database_data)
    return [insert_cell, database_data]

update_database(bullet_database, data_source)
plot_sheet.update_plotter(bullet_database, "2020-8-13")