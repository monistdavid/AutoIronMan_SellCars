from flask import render_template, Blueprint, request, redirect, url_for, session
from datetime import datetime

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SPREADSHEET_ID = '1Mw0EzaYJxPvCUPPq3hnTQv9fdz3Sn9LCmqy50uVbnjc'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

ALLOWED_ELEMENTS = [
    "Odometer", "FrontSeats", "InteriorRoof", "DriverFrontDoor", "DriverApron",
    "PassengerApron", "DriverFrontCorner", "RearSeatArea", "Dashboard",
    "PassengerRearCorner", "TrunkArea", "PassengerSideQuarter", "DriverSideQuarter",
    "DriverRearWheel"
]


# update to google sheet
def update_google_sheet(sheet_name, list_info, changes_cols, vin):
    sheet_id = SPREADSHEET_ID
    creds = None
    if os.path.exists('util/token.json'):
        creds = Credentials.from_authorized_user_file('util/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('util/google_credential.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('util/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    # Get the existing data from the sheet
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    values = result.get('values', [])
    vin_column_index = values[0].index("VIN")

    # Search for the row with the given VIN
    row_index = None
    for i, row in enumerate(values):
        if len(row) > 2 and row[vin_column_index] == vin:  # Assuming VIN is in the third column (index 2)
            row_index = i + 1  # Sheets API uses 1-indexed rows

    if row_index:
        # VIN found, update the existing row
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f'{sheet_name}!{changes_cols[0]}{row_index}:{changes_cols[1]}{row_index}',
            valueInputOption='USER_ENTERED',
            body={
                'values': [list_info]
            }
        ).execute()
    else:
        # VIN not found, create a new row
        next_row = len(values) + 1
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f'{sheet_name}!{changes_cols[0]}{next_row}:{changes_cols[1]}{next_row}',
            valueInputOption='USER_ENTERED',
            body={
                'values': [list_info]
            }
        ).execute()


# update to google sheet
def update_google_sheet_car_offer(sheet_name, list_info, changes_cols, vin):
    sheet_id = SPREADSHEET_ID
    creds = None
    if os.path.exists('util/token.json'):
        creds = Credentials.from_authorized_user_file('util/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('util/google_credential.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('util/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    # Get the existing data from the sheet
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    values = result.get('values', [])
    vin_column_index = values[0].index("VIN")

    # Search for the row with the given VIN
    row_index = None
    for i, row in enumerate(values):
        if len(row) > 2 and row[vin_column_index] == vin:  # Assuming VIN is in the third column (index 2)
            row_index = i + 1  # Sheets API uses 1-indexed rows
    if row_index is None:
        return
    if row_index is not None:
        if values[row_index - 1][-3] != 'Pending':
            return

    if row_index:
        # VIN found, update the existing row
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f'{sheet_name}!{changes_cols[0]}{row_index}:{changes_cols[1]}{row_index}',
            valueInputOption='USER_ENTERED',
            body={
                'values': [list_info]
            }
        ).execute()


def create_folder_if_not_exists(parent_folder_id, folder_name):
    creds = None
    if os.path.exists('util/token.json'):
        creds = Credentials.from_authorized_user_file('util/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('util/google_credential.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('util/token.json', 'w') as token:
            token.write(creds.to_json())

    drive_service = build('drive', 'v3', credentials=creds)

    # Check if the folder already exists
    response = drive_service.files().list(q=f"'{parent_folder_id}' in parents and name='{folder_name}'",
                                          fields="files(id)").execute()
    items = response.get('files', [])

    if not items:
        # Create the folder if it doesn't exist
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id],
        }
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
        folder_metadata = drive_service.files().get(fileId=folder.get('id'), fields='webViewLink').execute()
        folder_url = folder_metadata.get('webViewLink')
        return folder_url, folder.get('id')
    else:
        folder_metadata = drive_service.files().get(fileId=items[0]['id'], fields='webViewLink').execute()
        folder_url = folder_metadata.get('webViewLink')
        return folder_url, items[0]['id']


def upload_image_to_drive(start_name, image_path, drive_folder_id):
    creds = None
    if os.path.exists('util/token.json'):
        creds = Credentials.from_authorized_user_file('util/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('util/google_credential.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('util/token.json', 'w') as token:
            token.write(creds.to_json())

    drive_service = build('drive', 'v3', credentials=creds)

    # List all files in the Drive folder
    response = drive_service.files().list(q=f"'{drive_folder_id}' in parents",
                                          fields="files(id, name)").execute()
    files = response.get('files', [])

    # Delete files with matching prefix
    for file in files:
        if file['name'].startswith(start_name):
            drive_service.files().delete(fileId=file['id']).execute()

    # Upload the image to the folder
    file_metadata = {
        'name': os.path.basename(image_path),
        'parents': [drive_folder_id],
    }
    media = MediaFileUpload(image_path, resumable=True)
    drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def drive_full_name(text):
    if text == '2':
        return '2WD'
    else:
        return '4WD/AWD'


def transmission_full_name(text):
    if text == 'A':
        return 'Automatic'
    else:
        return 'Manual'


def condition_full_name(text):
    if text == 'O':
        return 'Outstanding - Exceptional Mechanical, exterior and interior condition with no visible wear; no reconditioning required.'
    elif text == 'C':
        return "Clean - Minimal wear and tear with no major mechanical or cosmetic problems; may require limited reconditioning."
    elif text == 'A':
        return "Average - Normal wear and tear. May have a few mechanical and/or cosmetic problems and may require some reconditioning."
    elif text == 'R':
        return "Rough - Several mechanical and/or cosmetic problems requiring repairs."
    else:
        return "Damaged - Major mechanical and/or body damage that may render it in non-safe running condition."


def engine_issues_full_name(text):
    if text == 'E':
        return "Engine noise"
    elif text == 'R':
        return "Runs improperly"
    else:
        return "No runner"


def transmission_issues_full_name(text):
    if text == 'C':
        return "Clutch needs service"
    elif text == 'M':
        return "Missing gear"
    elif text == 'N':
        return "Not engaging"
    elif text == 'S':
        return "Shifts hard"
    else:
        return "Slipping"


def how_many_full_name(text):
    if text == 'O':
        return "One"
    elif text == 'T':
        return "Two"
    else:
        return "Three or more"


def warning_lights_full_name(text, other_info):
    if text == 'C':
        return "Check engine"
    elif text == 'A':
        return "ABS/Brakes"
    elif text == '4':
        return "4x4 needs repair"
    elif text == 'Ai':
        return "Airbag"
    elif text == 'T':
        return "Transmission"
    else:
        return "Other: " + other_info


def rust_full_name(text):
    if text == 'Yb':
        return "Yes - on the body"
    else:
        return "Yes - on the undercarriage"


# =================================================== carmax auto ==================================================
# import library
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime, timedelta
import requests

HOSTNAME = 'us.smartproxy.com'
PORT = '10000'
DRIVER = 'CHROME'
twilio = '21CfFIy5B9iSsDTHcmPfWZncAdul6CTY_Vxm67wI'
aws = 'kEMC;gp;R6lmZJl8y$W9.fDUVt=i-!;P'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
GOOGLE_FORM_ID = '1627FyvV2AQcmE2gox9Kr0eNjz7q-yEHVly5fcglXhOs'
SPREADSHEET_ID = '1Mw0EzaYJxPvCUPPq3hnTQv9fdz3Sn9LCmqy50uVbnjc'


# use smart proxy
def smartproxy():
    options = generate_chrome_option()
    proxy_str = '{hostname}:{port}'.format(hostname=HOSTNAME, port=PORT)
    options.add_argument('--proxy-server={}'.format(proxy_str))
    return options


# generate config for chrome driver
def generate_chrome_option():
    chrome_options = Options()
    # chrome_options.add_argument("user-data-dir=/home/ec2-user/.config/google-chrome/Default")
    chrome_options.add_argument("user-data-dir=C:/Users/david/AppData/Local/Google/Chrome/User Data/Default")
    # chrome_options.add_argument("user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': r'C:\Users\Administrator\Desktop\Gentle_Carmen\web\download',
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    return chrome_options


# edit google forms
def get_info_from_sheet(sheet_name, vin):
    creds = None
    if os.path.exists('util/token.json'):
        creds = Credentials.from_authorized_user_file('util/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'util/google_credential.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('util/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=sheet_name).execute()
    result = result.get('values', [])
    vin_column_index = result[0].index("VIN")

    # Search for the row with the given VIN
    row_with_vin = None
    for row in result[1:]:
        if len(row) > 2 and row[vin_column_index] == vin:  # Assuming VIN is in the third column (index 2)
            row_with_vin = row
            break
    # Search for the row with the given VIN

    return row_with_vin


def get_col_from_sheet(sheet_name):
    creds = None
    if os.path.exists('util/token.json'):
        creds = Credentials.from_authorized_user_file('util/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'util/google_credential.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('util/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=sheet_name).execute()
    result = result.get('values', [])
    return result[0]
