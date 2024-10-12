from openpyxl import load_workbook

date = load_workbook("first_sheet_from_data.xlsx")
sheet = date.active

headers = [cell.value for cell in sheet[1]]
data = []

for row in sheet.iter_rows(min_row=2, values_only=True):
    row_dict = {header: (cell if cell is not None else "-") for header, cell in zip(headers, row)}
    data.append(row_dict)

print(data) # aici avem intr-o lista, fiecare linie din doc
print(len(data))