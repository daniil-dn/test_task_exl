from xlsxwriter import Workbook


def create_xlsx(in_data: list, id) -> str:
    file_name = f'{id}.xlsx'
    wb = Workbook(file_name)
    ws = wb.add_worksheet('users')
    for idx, x in enumerate(in_data):
        name = x[0]
        role = x[1]
        birth = x[2]
        ws.write(f"A{idx + 1}", name)
        ws.write(f"B{idx + 1}", role)
        ws.write(f"C{idx + 1}", birth)
    wb.close()
    return file_name


def get_file(file_path):
    f = open(f'./{file_path}', 'rb')
    return f
