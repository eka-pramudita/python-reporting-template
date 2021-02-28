# Import Packages
from dotenv import load_dotenv
from helpers import logger, gsheets, data_cleaning, db_connections, dates
import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from dateutil.relativedelta import relativedelta

# Load .env file
load_dotenv()

# Define Google Spreadsheets target
REPORT_TAB = 'Reporting Template'
REPORT_KEY = os.getenv('GENERAL_REPORTING')
log = logger.get_logger(REPORT_TAB)
client = gsheets.db_client(log)

# Timestamp
def curdate():
    now = dates.current_datetime_jkt().date()
    currentdate = pd.DataFrame(pd.Series([now])).transpose()
    # Push data to Google Spreadsheets
    gsheets.save_sheet(client, REPORT_KEY, REPORT_TAB, currentdate, 'B3', False)
curdate()

# How to query
query_sample = """SELECT 
        organization_id `Pharmacy ID`, 
        name `Pharmacy Name`, 
        livedDate `Lived Date`, 
        FirstOrderedDate `First Ordered Date` 
            FROM( 
            SELECT min(lived_date) livedDate, organization_id, name
            FROM(
            SELECT user_activation.organization_id, 
            date_format(convert_tz(user_activation.created_at, '+00:00', '+07:00'),'%Y/%m/%d') AS lived_date, 
            organization.name
            FROM swiperx_procurement.user_activation 
            LEFT JOIN swiperx_procurement.organization ON organization.id = user_activation.organization_id 
            WHERE user_activation.type = 'Pharmacy' AND organization_id NOT IN (3,805,809)
            AND user_activation.organization_id 
            IN (SELECT distinct organization_id from user_activation WHERE status = 'active')
            ) a 
            GROUP by organization_id ) b 
            LEFT JOIN( 
            SELECT pharmacy_id, MIN(OrderedDate) FirstOrderedDate  
            FROM( 
            SELECT pharmacy_id, date_format(CONVERT_TZ(purchase_order.ordered_at, '+00:00','+07:00'),'%Y/%m/%d') OrderedDate 
            FROM swiperx_procurement.purchase_order 
            WHERE purchase_order.deleted_at IS NULL AND pharmacy_id <> 3 AND purchase_order.ordered_at IS NOT NULL AND purchase_order.merged_to is null AND purchase_order.cancelled_at is null
            ) c 
            GROUP BY pharmacy_id 
            ) d 
            on d.pharmacy_id = b.organization_id 
            GROUP BY organization_id;"""
table_sample = data_cleaning.to_dataframe(db_connections.query_alltime(query_sample))

# Create a regular period table (ex: monthly)
up_qty = pd.DataFrame(pd.Series([1, 2, 8, 43, 223, 640, 1116, 1123]), columns=['PBF ID'])
yearmonth = pd.DataFrame(pd.Series(['2020-07', '2020-08', '2020-09']), columns=['PBF'])
# for i in range(len(yearmonth)): #TODO fill with desired looping tasks.

# Countifs example
len(table['Pharmacy ID'][(table['Ordered Date'] == daily['Date'][i]) & (table['Final Amount'] != 0)].unique())

# Sumifs example
round(sum(table['Final Amount'][(table['Ordered Date'] == daily['Date'][i])]))

# JSON Extraction Example
date_start, date_end = datetime(2020,1,1), datetime(2020,3,31)
po_update = """SELECT 
        po_id `PO ID`, 
        po_number `PO Number`, 
        ordered_date `Ordered Date`,
        or_net_amount `OR Net Amount`,
        up_net_amount `UP Net Amount`,
        or_status `OR Status`,
        up_status `UP Status`,
        poi `POI` 
        FROM(
    SELECT JSON_EXTRACT(poa.description, '$.id') AS po_id,
        po.po_number po_number,
        date_format(CONVERT_TZ(po.ordered_at, '+00:00', '+07:00'), '%Y-%m-%d') AS ordered_date,
        JSON_EXTRACT(poa.description, '$.status') AS or_status,
        po.status AS up_status,
        FORMAT(JSON_EXTRACT(poa.description, '$.net_amount'),2) AS or_net_amount,
        FORMAT(po.net_amount,2) AS up_net_amount,
        JSON_EXTRACT(poa.description, '$.purchase_order_item') AS poi 
        FROM purchase_order_activity poa 
    LEFT JOIN purchase_order po ON po.id = poa.purchase_order_id 
    WHERE poa.action = 'CREATE'
    AND date_format(convert_tz(po.ordered_at, '+00:00', '+07:00'), '%Y-%m-%d') >= %s 
    AND date_format(convert_tz(po.ordered_at, '+00:00', '+07:00'), '%Y-%m-%d') <= %s
    ) a 
    WHERE or_net_amount != up_net_amount and po_id not IN(11,336,451,452,629)"""
df_po_update = data_cleaning.to_dataframe(db_connections.query_timeframe(po_update, date_start, date_end))

for i in range(len(df_po_update["POI"])):
    df_po_update["POI"][i] = df_po_update["POI"][i].replace('[', '')
    df_po_update["POI"][i] = df_po_update["POI"][i].replace(']', '')
for i in range(len(df_po_update["POI"])):
    df_po_update["POI"][i] = df_po_update["POI"][i].split(', {')
for i in range(len(df_po_update["POI"])):
    for j in range(1, len(df_po_update["POI"][i])):
        df_po_update["POI"][i][j] = "{" + df_po_update["POI"][i][j]
poi = []
for i in range(len(df_po_update['POI'])):
    for j in range(len(df_po_update['POI'][i])):
        poi.append(json.loads(df_po_update['POI'][i][j]))
poi = pd.DataFrame(poi)
poi.columns = ["Quantity", "Net Price", "Product ID", "Discount Rate", "Selling Price", "PO ID","Temporary Availability"]
df_poi = poi

# Convert into proper date
table_lived['Lived Date'] = table_lived['Lived Date'].dt.date

# Fill NA
table_lived['First Ordered Date'] = table_lived['First Ordered Date'].fillna('')

# Convert to Yearweek and Yearmonth
table_lived['Year Week Lived'] = table_lived['Lived Date'].apply(lambda x: '{0}-{1}'.format(x.year, x.isocalendar()[1]))
table_lived['Year Month Lived'] = table_lived['Lived Date'].apply(lambda x: x.strftime('%B-%Y'))

# Load data from another Google Spreadsheets
credit_limit = gsheets.load_sheet(gsheets.swiperx_pt_client(log_credit),
                                   os.getenv("SWIPERX_PT_CREDIT_TABLE_ID"), CREDIT, "A1", "C2000")