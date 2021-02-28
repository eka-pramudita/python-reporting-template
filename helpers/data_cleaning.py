import pandas as pd
import numpy as np
import re
import json
from datetime import datetime
from helpers import dates


def to_dataframe(input_data):
    df = pd.DataFrame(input_data)
    df = df.replace(np.nan, '', regex=True)
    return df


def regexmatch_list(regex_list, df, column_match, new_column):
    df[new_column] = ""

    for x in range(len(df[column_match])):
        for i in range(len(regex_list)):
            if re.search(regex_list[i][0], df[column_match][x]):
                df[new_column][x] = regex_list[i][1]

    return df


def regexmatch_single(regex, df, column_match, new_column, result):
    df[new_column] = [result if re.search(regex, x) else 0 for x in df[column_match]]

    return df


def yearmonth(df, column_date):
    df["Year Month"] = df[column_date].str.slice(0, 4) + "-" + df[column_date].str.slice(5, 7)

    return df


def poi_json_parse(po_update, poi_column_name):
    for i in range(len(po_update[poi_column_name])):
        po_update[poi_column_name][i] = po_update[poi_column_name][i].replace('[', '')
        po_update[poi_column_name][i] = po_update[poi_column_name][i].replace(']', '')
    for i in range(len(po_update[poi_column_name])):
        po_update[poi_column_name][i] = po_update[poi_column_name][i].split(', {')
    for i in range(len(po_update[poi_column_name])):
        for j in range(1, len(po_update[poi_column_name][i])):
            po_update[poi_column_name][i][j] = "{" + po_update[poi_column_name][i][j]
    poi = []
    for i in range(len(po_update[poi_column_name])):
        for j in range(len(po_update[poi_column_name][i])):
            poi.append(json.loads(po_update[poi_column_name][i][j]))
    poi = pd.DataFrame(poi)
    poi.columns = ["Quantity", "Net Price", "Product ID", "Discount Rate", "Selling Price", "PO ID"
        , "Temporary Availability", "ID", "Product", "Created At", "Updated At", "Purchase Order"]
    poi = poi.iloc[:, 0:7]

    return poi


def extract_date(df, column_date, new_column_date):
    df[new_column_date] = df[column_date].str.slice(0, 4) + "-" + df[column_date].str.slice(5, 7) + "-" + \
                          df[column_date].str.slice(8, 10)
    for i in range(len(df[new_column_date])):
        if df[new_column_date][i] != '--':
            df[new_column_date][i] = datetime.strptime(df[new_column_date][i], '%Y-%m-%d').date()
        else:
            df[new_column_date][i] = ''

    return df


def date_dif(df, column_date, new_column_date, end_date):
    df[new_column_date] = ""

    if end_date is None:
        end_date = dates.current_datetime_jkt().date()
    for i in range(len(df[column_date])):
        df[new_column_date][i] = (end_date - df[column_date][i]).days

    return df


def title_entire_column(df,column):
    for i in range(len(df[column])):
        df[column][i] = df[column][i].title()

    return df[column]


def str_to_int(df,column):
    for i in range(len(df[column])):
        df[column][i] = int(df[column][i])

    return df[column]