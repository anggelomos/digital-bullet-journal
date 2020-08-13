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