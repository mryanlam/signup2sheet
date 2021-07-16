from typing import List
import gspread

class gsheet_writer:
    def __init__(self, sheet_url:str):
        self.sheet = sheet_url

    def write_to_sheet(self, output_table: List[List[str]]):
        gc = gspread.service_account(filename='credentials.json')
        sh = gc.open_by_url(self.sheet).sheet1
        sh.update("A1", output_table)
        sh.format('A1:B1', {'textFormat': {'bold': True}})

