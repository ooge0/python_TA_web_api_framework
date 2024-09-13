import openpyxl


def get_row_count(path, sheet_name):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheet_name]
    return sheet.max_row


def get_column_count(path, sheet_name):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheet_name]
    return sheet.max_column


def get_cell_data(path, sheet_name, row_number: int, column_number: int):
    """
    Return cell data as single element. In case if cell data is NOT a text
    string returned value should be tuple or list.
    Pytest is using each character as input data for test that is why returned value
    should be not a string
    """
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheet_name]
    cell_data = sheet.cell(row=row_number, column=column_number).value
    return cell_data


def set_cell_data(path, sheet_name, row_number, column_number, data):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheet_name]
    sheet.cell(row=row_number, column=column_number).value = data
    workbook.save(path)


def get_data_as_list(path, sheet_name, flag=None):
    """
    Reads data from an Excel sheet and optionally filters by a 'valid_flag' column.

    Args:
        path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet.
        flag (bool, optional): If True, returns only rows where 'valid_flag' is True.
                               If False, returns only rows where 'valid_flag' is False.
                               If None, returns all rows.

    Returns:
        list: A list of lists, where each inner list represents a row of data.
    """

    final_list = []
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheet_name]
    row_count = sheet.max_row
    col_count = sheet.max_column

    for r in range(2, row_count + 1):
        row_data = []
        for c in range(1, col_count + 1):
            row_data.append(sheet.cell(row=r, column=c).value)

        # Check the flag in the first column (index 0)
        if flag is None or row_data[0] == flag:
            # Append the data excluding the first column
            final_list.append(row_data[1:])

    return final_list
