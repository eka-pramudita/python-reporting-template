import pygsheets

def db_client(log=None):
    client = pygsheets.authorize(service_account_env_var="GDRIVE_API_CREDENTIALS_EKA")
    if log:
        client.logger = log
    return client

def save_sheet(client, document_key, sheet_name, data, starting_cell, index):
    sheet = client.open_by_key(document_key)
    worksheet = sheet.worksheet_by_title(sheet_name)
    worksheet.set_dataframe(data, starting_cell, copy_head = index)


def load_sheet(client, document_key, sheet_name, cell_start, cell_end):
    sheet = client.open_by_key(document_key)
    worksheet = sheet.worksheet_by_title(sheet_name)
    data = worksheet.get_as_df(start=cell_start, end=cell_end)

    return data


def save_sheet_clear(client, document_key, sheet_name, data, starting_cell):
    sheet = client.open_by_key(document_key)
    worksheet = sheet.worksheet_by_title(sheet_name)
    worksheet.clear() #TODO edit to become area clear
    worksheet.set_dataframe(data, starting_cell)

def save_sheet_clear_partial(client, document_key, sheet_name, data, starting_cell, ending_cell, index):
    sheet = client.open_by_key(document_key)
    worksheet = sheet.worksheet_by_title(sheet_name)
    worksheet.clear(starting_cell, ending_cell) #TODO edit to become area clear
    worksheet.set_dataframe(data, starting_cell, copy_head = index)