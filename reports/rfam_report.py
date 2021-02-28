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
REPORT_KEY = os.getenv('RFAM_SAMPLE_REPORT')
REPORT_TAB_UPDATE = 'Last Update'
REPORT_TAB_DATA = 'Data'
log_update = logger.get_logger(REPORT_TAB_UPDATE)
log_data = logger.get_logger(REPORT_TAB_DATA)
client_update = gsheets.db_client(log_update)
client_data = gsheets.db_client(log_data)

# Timestamp
def curdate():
    now = dates.current_datetime_jkt().strftime('%Y-%m-%d %H:%M:%S')
    currentdate = pd.DataFrame(pd.Series([now])).transpose()
    # Push data to Google Spreadsheets
    gsheets.save_sheet(client_update, REPORT_KEY, REPORT_TAB_UPDATE, currentdate, 'B1', False)
curdate()

# RNA Samples Generated
query_rfam = """select 	date_format(created, '%Y') `Year`, count(rfam_id) `Samples Generated`
                from 	family
                where 	date(created) >= '2014-01-01'
                group by 	date_format(created, '%Y')
                order by created ASC"""
table_rfam = data_cleaning.to_dataframe(db_connections.query_alltime(query_rfam))
# Data Cleaning - take first 5 rows and 2 columns
#table_rfam = table_rfam.iloc[0:30,]
gsheets.save_sheet_clear_partial(client_data, REPORT_KEY, REPORT_TAB_DATA, table_rfam, 'A1','B',True)

# Top Contributed Author
query_author = """select author, count(author) sample_number
                from family
                group by author
                order by count(author) desc
                limit 10"""
table_author = data_cleaning.to_dataframe(db_connections.query_alltime(query_author))
# Data Cleaning - take first 5 rows and 2 columns
gsheets.save_sheet_clear_partial(client_data, REPORT_KEY, REPORT_TAB_DATA, table_author, 'D1','E',True)

# RNA Match Pair Node
query_match = """  select match_pair_node, count(match_pair_node) number_matched
                    from family
                    group by match_pair_node"""
table_match = data_cleaning.to_dataframe(db_connections.query_alltime(query_match))
# Data Cleaning - take first 5 rows and 2 columns
gsheets.save_sheet_clear_partial(client_data, REPORT_KEY, REPORT_TAB_DATA, table_match, 'G1','H',True)