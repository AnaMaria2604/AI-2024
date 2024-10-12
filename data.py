from openpyxl import load_workbook

date = load_workbook("first_sheet_from_data.xlsx")
sheet = date.active

headers = [cell.value for cell in sheet[1]]

filtered_headers = headers[2:]

data = []

for row in sheet.iter_rows(min_row=2, values_only=True):
    row_dict = {header: (cell if cell is not None else "-") for header, cell in zip(filtered_headers, row[2:])}
    data.append(row_dict)

print(data)
print(f"lungime veche: {len(data)}")

data_without_duplicates = []
for i in data:
    if i not in data_without_duplicates:
        data_without_duplicates.append(i)

print(f"lungime noua: {len(data_without_duplicates)}")

