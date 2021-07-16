from typing import List

class gsheet_writer:
    def __init__(self, sheet_url:str):
        self.sheet = sheet_url

    def write_to_sheet(self, output_table: List[List[str]]):
        pass


