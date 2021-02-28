# Reporting Template
###### by Eka Pramudita

## Requirements 
- Python 3.8
- Pandas
- Numpy
- Pygsheets
- MySQL Connector Python
- Python Dotenv

## Installation

```.bash
pip install -r requirements.txt
```
## Configuration

#### ENV
Configuration trough ENV variables. `.env` file is supported. Example provided in: `env.example`

#### Setting PYTHONPATH
Example:
```
export PYTHONPATH="/Users/greg/projects/python-db/"
```
#### Run single script
```
python ./src/aggregations/swiperx_new_users.py [params]
```

## Scheduler - Crontab
Scheduler is located in file: `/crontab`

## Directory structure
```
.
├── aggregations/     <- Python sripts generating aggregates from multiple sources 
├── helpers/          <- Reusable functions like db connections, .etc
├── reports/          <- Python scripts to generate and store reports
├── crontab          <- scheduler file
├── README.md        <- This file
```



## Reports
### Connecting Database
- Store Host, Port, User, Password, and Name of the database in .env file
- Create a python file (named db_connections.py) in helpers folder containing functions to pull the data from the database
- Import modules needed in the db_connections.py:
```
import mysql.connector
import os
```
- Set up a function to connect the database:
```
def db_con():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_DATABASE"))
```
- With the connector, now we can pull the data from 
the database using MySQL query put in the ```sql``` variable. We can set up a full query
or a time-limited query. Full query:
```
def query_alltime(sql):
    connection = db_con()
    cursor = connection.cursor(dictionary=True, buffered=True)

    cursor.execute(sql)
    res = cursor.fetchall()
    connection.close()
    return res
```
Time-limited query:
```
def query_timeframe(sql,date_start,date_end):
    connection = swiperx_pt_db_con()
    cursor = connection.cursor(dictionary=True, buffered=True)
    date_start = date_start.strftime('%Y-%m-%d')
    date_end = date_end.strftime('%Y-%m-%d')
    cursor.execute(sql, (date_start, date_end))
    res = cursor.fetchall()
    connection.close()
    return res
```
Note: to perform a time-limited query, we need to put date marker
in our query like this:
```
AND date_format(convert_tz(po.ordered_at, '+00:00', '+07:00'), '%Y-%m-%d') >= %s 
AND date_format(convert_tz(po.ordered_at, '+00:00', '+07:00'), '%Y-%m-%d') <= %s
```

### Linking Python to the Google Spreadsheets
- Enable Google Drive API and Google Spreadsheets API in the Google APIs page: https://console.developers.google.com/
- Go to Credentials, create credentials, and choose Service Account
- Get the key stored in JSON format (If there is any error when trying to connect, create another Service Account and add key)
- Store the key to .env file in one-line string started and ended with ```'```
- Create a python file to set up gsheet connection (named gsheets.py)
- Import pygsheets there
- Define a client function to connect:
```
def db_client(log=None):
    client = pygsheets.authorize(service_account_env_var="GDRIVE_API_CREDENTIALS_EKA")
    if log:
        client.logger = log
    return client
```
- Create functions that are frequently used such as: Save Sheets, Load Sheets, Save Sheets Clear, etc.
```
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
```

## Automation Setting
### Windows Task Scheduler
1. Open Windows Task Scheduler, then Create a Task
2. In menu "General", give task a name
3. In menu "Triggers", set up the schedule of running
4. In menu "Action", you need to fill Program/Script and Add Arguments.
Fill Program/Script with the directory of python.exe you installed.
Fill Add Arguments with the directory of python file you want to run.
5. Copy all self-created modules to .../Lib/site-packages folder in your installed Python folder.
6. Wait the program to run according to your schedule, or run the program from directly.
7. If there's some errors, check it on the command prompt by copying what you fill on Program/Script (space) Add Arguments

### Airflow


## Aggregates

