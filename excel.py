import xlrd
from datetime import date, time

def read_excel_from_bytes(bytes):
    book = xlrd.open_workbook(file_contents=bytes)
    print(book.sheet_names())
    sheet = book.sheet_by_index(0)
    print(sheet.nrows)
    print(sheet.ncols)
    data = []
    headers = [sheet.cell_value(0,i) for i in range(0,sheet.ncols)]
    data.append(headers)

    for nrow in range(1,sheet.nrows):
        row = []
        for ncol in range(0,sheet.ncols):
            value = sheet.cell_value(nrow, ncol)
            # 3 - дата
            if sheet.cell_type(nrow, ncol) == 3:
                t = xlrd.xldate_as_tuple(value,0)
                value = date(year=t[0],month=t[1], day=t[2])
            row.append(value)
        data.append(row)

    return data
