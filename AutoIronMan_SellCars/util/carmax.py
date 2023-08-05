import time
from selenium.webdriver.common.by import By
from selenium import webdriver
# from webTest.util import utils
from util import utils
from selenium.webdriver.support.select import Select
import os
import undetected_chromedriver as uc
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

USERNAME = 'JOEY@GENTLECARMEN.COM'
PASSWORD = 'Yaodan0117$$'
VIN = '4T4BF1FK9GR553904'
CURRENT_MILEAGE = '43000'
MILE_OPTION = 'Actual Miles'
TRIM = 'XSE 4D Sedan 2.5L 4 CYL (Gas) Automatic 2WD'
DRIVE = '2WD'
TRANSMISSION = 'A'
AVAILABLE_FEATURES = ['Entune', 'JBL Sound System']
CONDITIONS = 'Outstanding'
IN_ACCIDENT = 'false'
MECHANICAL_ISSUES = ['AC issues', 'Brake issues']
ENGINE = 'false'
TRANSMISSION_ISSUE = 'false'
BODY_PAINT = 'false'
WARNINGLIGHTS = 'false'
RUST = 'false'
INTERIOR = 'false'
VEHICLELIFTED = 'false'
ENGINEMODIFIED = 'false'
INTERIORISSUES = 'false'
TIRESREPLACED = 'false'

ALLOWED_ELEMENTS = [
    "Odometer", "PassengerApron", "DriverApron", "DriverFrontCorner", "PassengerRearCorner", "TrunkArea",
    "DriverSideQuarter", "PassengerSideQuarter", "DriverRearWheel", "RearSeatArea", "Dashboard",
    "FrontSeats", "DriverFrontDoor", "InteriorRoof"
]


# login to carmax
def log_in(browser):
    browser.get('https://www.carmax.com/maxoffer')
    time.sleep(2)

    user_name_box = browser.find_element(By.XPATH, '//input[@name="Email"]')
    pass_word_box = browser.find_element(By.XPATH, '//input[@name="Password"]')

    user_name_box.send_keys(USERNAME)
    pass_word_box.send_keys(PASSWORD)
    time.sleep(1)

    # define submit button
    submit_button = browser.find_element(By.XPATH,
                                         '//button[@id="next" and @type="submit" and @form="localAccountForm"]')
    submit_button.click()
    time.sleep(10)


def get_offer():
    # chrome_options = utils.generate_chrome_option()
    # browser = webdriver.Chrome(options=chrome_options)

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-dev-shm-usage')

    browser = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        log_in(browser)
    except:
        print("Already logged in")

    print(browser.title)
    # try to go back to the start page
    live_trade = browser.find_element(By.XPATH, '//h2[text()="View my Dashboard"]')
    live_trade.click()
    time.sleep(2)

    select_open = browser.find_element(By.XPATH, "//button[@id='open-tab']")
    select_open.click()
    time.sleep(2)

    table_body = browser.find_element(By.CLASS_NAME, 'MuiTableBody-root')

    # Find all rows within the table body
    rows = table_body.find_elements(By.CLASS_NAME, 'MuiTableRow-root')

    # Loop through each row and extract the information
    for index, row in enumerate(rows):
        # Check if the row index is even (since the enumeration starts from 0)
        if index % 2 == 0:
            columns = row.find_elements(By.CLASS_NAME, 'MuiTableCell-body')

            # Extract and print the specific columns you need
            expiration_time = columns[1].text
            vin = columns[3].text
            price = columns[4].text
            print(expiration_time)
            utils.update_google_sheet_car_offer('Form Responses 1', [expiration_time, price], ['AD', 'AE'], vin)


def get_redeem_offer(vin_input):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-dev-shm-usage')

    browser = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        log_in(browser)
    except:
        print("Already logged in")

    # try to go back to the start page
    live_trade = browser.find_element(By.XPATH, '//h2[text()="Redeem a CarMax offer"]')
    live_trade.click()
    time.sleep(2)

    try:
        restart = browser.find_element(By.XPATH,
                                       "//button[@class='MuiButtonBase-root MuiIconButton-root close-button']")
        restart.click()
        print("Start over")
    except:
        print("starting")

    enter_vin = browser.find_element(By.XPATH, '//input[@id="text-field-text-field-license"]')
    enter_vin.send_keys("\b" * len(enter_vin.get_attribute("value")))
    enter_vin.send_keys(vin_input)
    time.sleep(5)

    try:
        # try to go back to the start page
        view_redeem_offer = browser.find_element(By.XPATH, "//hzn-button[contains(text(), 'View offer')]")
        view_redeem_offer.click()
        time.sleep(4)
        offer_value = browser.find_element(By.XPATH, "//p[@class='kmx-typography--display-2 fs-mask']")
        expiration_date = browser.find_element(By.XPATH, "//p[@class='kmx-typography--display-1 offer__expires']")
        utils.update_google_sheet('Form Responses 1',
                                  [offer_value.text + ' ' + expiration_date.text], ['AG', 'AG'], vin_input)
        print("Found an offer")
    except:
        utils.update_google_sheet('Form Responses 1', ['Not found'], ['AG', 'AG'], vin_input)
        print("Offer not found")
    browser.close()


def submit_form(vin_input):
    # chrome_options = utils.generate_chrome_option()
    # browser = webdriver.Chrome(options=chrome_options)

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-dev-shm-usage')

    browser = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        log_in(browser)
    except:
        print("Already logged in")
    info = utils.get_info_from_sheet('Form Responses 1', vin_input)
    all_col = utils.get_col_from_sheet('Form Responses 1')

    VIN = info[all_col.index("VIN")]
    CURRENT_MILEAGE = info[all_col.index("Current Mileage")]
    MILE_OPTION = info[all_col.index("Current Mileage Option")]
    # TRIM = 'Premium Plus 4D Sport Utility 3.0L 6 CYL (Hybrid) Automatic 4WD/AWD'
    DRIVE = '2WD' if info[all_col.index("Drive")] == '2WD' else '4WD'
    TRANSMISSION = 'A' if info[all_col.index("Transmission")] == 'Automatic' else 'MANUAL'
    # AVAILABLE_FEATURES = info[6].split(',')
    CONDITIONS = info[all_col.index("What is the overall condition of the vehicle?")]
    IN_ACCIDENT = 'true' if info[all_col.index("Has the vehicle ever been in an accident?")] == 'Yes' else 'false'
    MECHANICAL_ISSUES = info[all_col.index("Are there any mechanical or other issues present?")].split(';')
    ENGINE = info[all_col.index("Are there any issues noted with the engine?")].split(';') if info[all_col.index(
        "Are there any issues noted with the engine?")] != 'No' else 'false'
    TRANSMISSION_ISSUE = info[all_col.index("Are there any issues noted with the transmission?")].split(';') if \
        info[all_col.index("Are there any issues noted with the transmission?")] != 'No' else 'false'
    BODY_PAINT = info[all_col.index("Are there any panels in need of paint or body work?")] if \
        info[all_col.index("Are there any panels in need of paint or body work?")] != 'No' else 'false'
    WARNINGLIGHTS = info[all_col.index("Are there any warning lights currently on?")].split(';') if \
        info[all_col.index("Are there any warning lights currently on?")] != 'No' else 'false'
    RUST = info[all_col.index("Is there any perforating rust present on the vehicle?")] if \
        info[all_col.index("Is there any perforating rust present on the vehicle?")] != 'No' else 'false'
    INTERIOR = info[all_col.index("Are any interior parts broken or inoperable?")] \
        if info[all_col.index("Are any interior parts broken or inoperable?")] != 'No' else 'false'
    VEHICLELIFTED = 'true' if info[all_col.index("Has the vehicle been lifted or lowered?")] == 'Yes' else 'false'
    ENGINEMODIFIED = 'true' if info[all_col.index("Have engine modifications been made?")] == 'Yes' else 'false'
    INTERIORISSUES = info[all_col.index("Are there any interior parts with rips, tears, or stains?")] if \
        info[all_col.index("Are there any interior parts with rips, tears, or stains?")] != 'No' else 'false'
    TIRESREPLACED = info[all_col.index("Do any tires need to be replaced?")] if \
        info[all_col.index("Do any tires need to be replaced?")] != 'No' else 'false'

    # Print all the variables
    print(f"VIN: {VIN}")
    print(f"Current Mileage: {CURRENT_MILEAGE}")
    print(f"Current Mileage Option: {MILE_OPTION}")
    print(f"Drive: {DRIVE}")
    print(f"Transmission: {TRANSMISSION}")
    print(f"Overall Condition: {CONDITIONS}")
    print(f"Has been in an accident: {IN_ACCIDENT}")
    print(f"Mechanical or other issues: {MECHANICAL_ISSUES}")
    print(f"Issues noted with the engine: {ENGINE}")
    print(f"Issues noted with the transmission: {TRANSMISSION_ISSUE}")
    print(f"Panels in need of paint or body work: {BODY_PAINT}")
    print(f"Warning lights currently on: {WARNINGLIGHTS}")
    print(f"Perforating rust present on the vehicle: {RUST}")
    print(f"Interior parts broken or inoperable: {INTERIOR}")
    print(f"Vehicle lifted or lowered: {VEHICLELIFTED}")
    print(f"Engine modifications made: {ENGINEMODIFIED}")
    print(f"Interior parts with rips, tears, or stains: {INTERIORISSUES}")
    print(f"Tires need to be replaced: {TIRESREPLACED}")
    # ==================================================== clean history ==============================================

    # try to go back to the start page
    live_trade = browser.find_element(By.XPATH, '//h2[text()="Send a live trade or aged unit"]')
    live_trade.click()
    time.sleep(2)

    while True:
        try:
            browser.find_element(By.XPATH, '//button[@id="back-button-icon"]').click()
            print("Going back....")
        except:
            break
    time.sleep(2)

    # # try to go back to the start page
    # browser.find_element(By.XPATH, '//button[@data-testid="appraisal-action-icon"]').click()
    # time.sleep(3)
    #
    # browser.find_element(By.XPATH, '//li[@data-testid="Clear Cache"]').click()
    # print("Going back....")
    # time.sleep(2)

    # start to input the information
    # ===================================== select VIN and start ==================================================
    live_trade = browser.find_element(By.XPATH, '//h2[text()="Send a live trade or aged unit"]')
    live_trade.click()
    time.sleep(2)

    vin = browser.find_element(By.XPATH, '//label[text()="VIN"]')
    vin.click()
    time.sleep(2)

    enter_vin = browser.find_element(By.XPATH, '//input[@id="text-field-text-field-license"]')
    enter_vin.send_keys("\b" * len(enter_vin.get_attribute("value")))
    enter_vin.send_keys(VIN)
    time.sleep(2)

    # custom_waiting = browser.find_element(By.XPATH, '//input[@value="true"]')
    custom_waiting = browser.find_element(By.XPATH, '//input[@value="false"]')
    custom_waiting.click()
    time.sleep(2)

    start = browser.find_element(By.XPATH, '//hzn-button[text()="Get started"]')
    start.click()
    time.sleep(2)

    start_continue = browser.find_element(By.XPATH,
                                          '//hzn-button[contains(@class, "validate-ymm__continue continue-button")]')
    start_continue.click()
    time.sleep(2)

    # =================================================input car information===========================================
    print("Putting car info...")
    try:
        current_mileage = browser.find_element(By.XPATH, '//input[@name="current-mileage"]')
        current_mileage.send_keys("\b" * len(current_mileage.get_attribute("value")))
        current_mileage.send_keys(CURRENT_MILEAGE)
        time.sleep(2)
    except:
        return "Error: current_mileage"

    try:
        mile_option = browser.find_element(By.XPATH, f'//label[text()="{MILE_OPTION}"]')
        mile_option.click()
        time.sleep(2)
    except:
        return "Error: mile_option"

    try:
        trim = browser.find_element(By.ID, "select-trim")
        select = Select(trim)
        # select.select_by_value(TRIM)
        select.select_by_index(1)
        time.sleep(2)
    except:
        return "Error: trim"

    try:
        drive = browser.find_element(By.ID, "select-drivetrain")
        select = Select(drive)
        select.select_by_value(DRIVE)
        time.sleep(2)
    except:
        return "Error: drive"

    try:
        # Find the <select> element by its ID or any other appropriate method
        transmission = browser.find_element(By.ID, "select-transmissionType")
        select = Select(transmission)
        select.select_by_value(TRANSMISSION)
        time.sleep(2)
    except:
        return "Error: transmission"

    try:
        for feature in AVAILABLE_FEATURES:
            try:
                feature = browser.find_element(By.XPATH, f'//label[text()="{feature}"]')
                feature.click()
                time.sleep(2)
            except:
                pass
    except:
        return "Error: features"

    try:
        conditions = browser.find_element(By.XPATH, f'//*[contains(text(), "{CONDITIONS}")]')
        conditions.click()
        time.sleep(2)
    except:
        return "Error: conditions"

    try:
        accident = browser.find_element(By.XPATH, f'//input[@name="accident-{IN_ACCIDENT}" and @value="{IN_ACCIDENT}"]')
        accident.click()
        time.sleep(2)
    except:
        return "Error: accident"

    try:
        for mechanical in MECHANICAL_ISSUES:
            if 'Other issues' in mechanical:
                mec = browser.find_element(By.XPATH, f'//label[text()="Other issues"]')
                mec.click()
                time.sleep(2)
                mec = browser.find_element(By.XPATH, '//input[@name="mechanicalOtherIssuesExplain"]')
                index = mechanical.find("Other issues: ")
                mec.send_keys(mechanical[index + len("Other issues: "):])
            else:
                mechanical = browser.find_element(By.XPATH, f'//label[text()="{mechanical}"]')
                mechanical.click()
                time.sleep(2)
    except:
        return "Error: mechanical_issues"

    try:
        if ENGINE == 'false':
            engine = browser.find_element(By.XPATH,
                                          f'//input[@name="engineIssuesRadio-{ENGINE}" and @value="{ENGINE}"]')
            engine.click()
        else:
            engine = browser.find_element(By.XPATH, f'//input[@name="engineIssuesRadio-true" and @value="true"]')
            engine.click()
            for eng in ENGINE:
                eng = browser.find_element(By.XPATH, f'//label[text()="{eng}"]')
                eng.click()
                time.sleep(2)
        time.sleep(2)
    except:
        return "Error: engine"

    try:
        if TRANSMISSION_ISSUE == 'false':
            transmission_issue = browser.find_element(By.XPATH,
                                                      f'//input[@name="transmissionIssuesRadio-{TRANSMISSION_ISSUE}" and @value="{TRANSMISSION_ISSUE}"]')
            transmission_issue.click()
        else:
            transmission_issue = browser.find_element(By.XPATH,
                                                      f'//input[@name="transmissionIssuesRadio-true" and @value="true"]')
            transmission_issue.click()
            time.sleep(2)
            for tra in TRANSMISSION_ISSUE:
                tra = browser.find_element(By.XPATH, f'//label[text()="{tra}"]')
                tra.click()
                time.sleep(2)
        time.sleep(2)
    except:
        return "Error: transmission_issue"

    try:
        if BODY_PAINT == 'false':
            body_paint = browser.find_element(By.XPATH,
                                              f'//input[@name="paintBodyWorkRadio-{BODY_PAINT}" and @value="{BODY_PAINT}"]')
            body_paint.click()
            time.sleep(2)
        else:
            body_paint = browser.find_element(By.XPATH,
                                              f'//input[@name="paintBodyWorkRadio-true" and @value="true"]')
            body_paint.click()
            time.sleep(2)
            body_paint = browser.find_element(By.ID, "select-paintBodyWork")
            select = Select(body_paint)
            if BODY_PAINT == 'One':
                select.select_by_value('ONE')
            elif BODY_PAINT == 'Two':
                select.select_by_value('TWO')
            else:
                select.select_by_value('THREEPLUS')
            time.sleep(2)
    except:
        return "Error: body_paint"

    try:
        if WARNINGLIGHTS == 'false':
            warningLights = browser.find_element(By.XPATH,
                                                 f'//input[@name="warningLightsRadio-{WARNINGLIGHTS}" and @value="{WARNINGLIGHTS}"]')
            warningLights.click()
            time.sleep(2)
        else:
            warningLights = browser.find_element(By.XPATH,
                                                 f'//input[@name="warningLightsRadio-true" and @value="true"]')
            warningLights.click()
            time.sleep(2)
            for tra in WARNINGLIGHTS:
                warningLights = browser.find_element(By.XPATH, f'//label[text()="{tra}"]')
                warningLights.click()
                time.sleep(2)
    except:
        return "Error: warninglights"

    try:
        if RUST == 'false':
            rust = browser.find_element(By.XPATH,
                                        f'//input[@name="rustRadio-{RUST}" and @value="{RUST}"]')
            rust.click()
            time.sleep(2)
        else:
            rust = browser.find_element(By.XPATH,
                                        f'//input[@name="rustRadio-true" and @value="true"]')
            rust.click()
            time.sleep(2)
            rust = browser.find_element(By.XPATH, f'//label[text()="{RUST}"]')
            rust.click()
            time.sleep(2)
    except:
        return "Error: rust"

    try:
        if INTERIOR == 'false':
            interior = browser.find_element(By.XPATH,
                                            f'//input[@name="interiorPartsIssuesRadio-{INTERIOR}" and @value="{INTERIOR}"]')
            interior.click()
            time.sleep(2)
        else:
            interior = browser.find_element(By.XPATH,
                                            f'//input[@name="interiorPartsIssuesRadio-true" and @value="true"]')
            interior.click()
            time.sleep(2)
            interior = browser.find_element(By.ID, "select-interiorPartsIssues")
            select = Select(interior)
            if INTERIOR == 'One':
                select.select_by_value('ONE')
            elif INTERIOR == 'Two':
                select.select_by_value('TWO')
            else:
                select.select_by_value('THREEPLUS')
            time.sleep(2)
    except:
        return "Error: interior issue"

    try:
        vehicleLifted = browser.find_element(By.XPATH,
                                             f'//input[@name="vehicleLiftedLowered-{VEHICLELIFTED}" and @value="{VEHICLELIFTED}"]')
        vehicleLifted.click()
        time.sleep(2)
    except:
        return "Error: vehicle lifted"

    try:
        engineModified = browser.find_element(By.XPATH,
                                              f'//input[@name="engineModified-{ENGINEMODIFIED}" and @value="{ENGINEMODIFIED}"]')
        engineModified.click()
        time.sleep(2)
    except:
        return "Error: engine modified"

    try:
        if INTERIORISSUES == 'false':
            interiorIssues = browser.find_element(By.XPATH,
                                                  f'//input[@name="interiorIssuesRadio-{INTERIORISSUES}" and @value="{INTERIORISSUES}"]')
            interiorIssues.click()
            time.sleep(2)
        else:
            interiorIssues = browser.find_element(By.XPATH,
                                                  f'//input[@name="interiorIssuesRadio-true" and @value="true"]')
            interiorIssues.click()
            time.sleep(2)
            interiorIssues = browser.find_element(By.ID, "select-interiorIssues")
            select = Select(interiorIssues)
            if INTERIORISSUES == 'One':
                select.select_by_value('ONE')
            elif INTERIORISSUES == 'Two':
                select.select_by_value('TWO')
            else:
                select.select_by_value('THREEPLUS')
            time.sleep(2)
    except:
        return "Error: interior part issues"

    try:
        if TIRESREPLACED == 'false':
            tiresReplaced = browser.find_element(By.XPATH,
                                                 f'//input[@name="tiresReplacedRadio-{TIRESREPLACED}" and @value="{TIRESREPLACED}"]')
            tiresReplaced.click()
            time.sleep(2)
        else:
            tiresReplaced = browser.find_element(By.XPATH,
                                                 f'//input[@name="tiresReplacedRadio-true" and @value="true"]')
            tiresReplaced.click()
            time.sleep(2)
            tiresReplaced = browser.find_element(By.ID, "select-tiresReplaced")
            select = Select(tiresReplaced)
            if TIRESREPLACED == 'One':
                select.select_by_value('ONE')
            elif TIRESREPLACED == 'Two':
                select.select_by_value('TWO')
            else:
                select.select_by_value('THREEPLUS')
            time.sleep(2)
    except:
        return "Error: tire replaced"

    continue_button = browser.find_element(By.XPATH, '//hzn-button[@class="vehicle-details__continue"]')
    continue_button.click()
    time.sleep(2)

    # =================================================== upload image ================================================
    try:
        print('Uploading car image...')
        for i in range(1, 15):
            number = str(i)
            upload_image = browser.find_element(By.XPATH, f'//input[@data-testid="input-upload-gallery-{number}"]')
            element = ALLOWED_ELEMENTS[i - 1]
            valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.PNG', '.JPG', '.JPEG', '.GIF']
            absolute_path = 'C:/Users/david/Desktop/work/David-Alex/Gentla_Carmen_Carmax/web2/static/images/' + str(
                vin_input) + '/' + element
            element_path = 'static/images/' + str(vin_input) + '/' + element
            for ext in valid_extensions:
                if os.path.exists(element_path + ext):
                    # upload_image.send_keys(
                    #     "C:/Users/david/Desktop/work/David-Alex/Gentle_Carmen_Carmax/web2/static/images/" + str(
                    #         vin_input) + '/' + element + ext)
                    upload_image.send_keys(
                        "/home/ubuntu/Gentle_Carmen_Carmax/web2/static/images/" + str(vin_input) + '/' + element + ext)
                    # upload_image.send_keys("C:/Users/david/Desktop/work/David-Alex/Gentle_Carmen_Carmax/web2/static/images/4T4BF1FK9GR553904/Odometer.png")
                    break
            time.sleep(5)
    except:
        browser.close()
        return "Error: image issue"

    continue_button = browser.find_element(By.XPATH, '//hzn-button[text()="Continue"]')
    continue_button.click()
    time.sleep(5)

    # =================================================== submit application ===========================================
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submit_button = browser.find_element(By.XPATH, "//hzn-button[text()='Submit']")
    submit_button.click()
    time.sleep(2)
    print("Submitted")
    browser.close()
    return "Pending"
