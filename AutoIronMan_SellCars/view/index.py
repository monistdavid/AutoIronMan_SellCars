from flask import render_template, Blueprint, request, redirect, url_for, session
from datetime import datetime
import os
from webTest.util import utils, carmax
# from util import utils, carmax
import vinlib

SPREADSHEET_ID = '1Mw0EzaYJxPvCUPPq3hnTQv9fdz3Sn9LCmqy50uVbnjc'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

ALLOWED_ELEMENTS = [
    "Odometer", "FrontSeats", "InteriorRoof", "DriverFrontDoor", "DriverApron",
    "PassengerApron", "DriverFrontCorner", "RearSeatArea", "Dashboard",
    "PassengerRearCorner", "TrunkArea", "PassengerSideQuarter", "DriverSideQuarter",
    "DriverRearWheel"
]

index_bp = Blueprint('index', __name__)


@index_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        form_data = session.get("form_data", {})
        return render_template('index.html', form_data=form_data)
    else:
        # Handle form submission and store the form data in the session
        input_mail = request.form.get("input-mail")
        input_phone = request.form.get("input-phone")
        input_name = request.form.get("input-name")
        input_vin = request.form.get("input-vin")
        input_rep = request.form.get("input-rep")
        input_zip = request.form.get("input-zip")
        title_status = request.form.get("title-status")
        sell_time = request.form.get("sell-time")
        try:
            if session["form_data"]:
                session["form_data"]["input-mail"] = input_mail
                session["form_data"]["input-vin"] = input_vin
                session["form_data"]["input-name"] = input_name
                session["form_data"]["input-vin"] = input_vin
                session["form_data"]["input-rep"] = input_rep
                session["form_data"]["input-zip"] = input_zip
                session["form_data"]["title-status"] = title_status
                session["form_data"]["sell-time"] = sell_time
                session.modified()
        except:
            session["form_data"] = {
                "input-mail": input_mail,
                "input-phone": input_phone,
                "input-name": input_name,
                "input-vin": input_vin,
                "input-rep": input_rep,
                "input-zip": input_zip,
                "title-status": title_status,
                "sell-time": sell_time
            }

        current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        if input_vin is not None:
            if vinlib.check_vin(input_vin):
                utils.update_google_sheet('Form Responses 1',
                                          [current_time, input_mail, input_phone, input_name, input_rep,
                                           "'" + str(input_zip), title_status, sell_time, input_vin],
                                          ['A', 'I'], input_vin)
            else:
                error_message = "(VIN 码不正确，请重新填写)"
                form_data = session.get("form_data", {})
                print(form_data)
                return render_template('index.html', form_data=form_data, error_message=error_message)

        print("Basic")
        if input_vin is None:
            form_data = session.get("form_data", {})
            print(form_data)
            return render_template('index.html', form_data=form_data)
        return redirect(url_for('index.vehicle', vin=input_vin))


@index_bp.route('/vehicle/<string:vin>', methods=["GET", "POST"])
def vehicle(vin):
    if request.method == "GET":
        form_data = session.get("form_data", {})
        return render_template('vehicle.html', form_data=form_data, vin=vin)
    else:
        print("vehicle")
        input_mile = request.form.get("input-mile")
        mile_disclosure = request.form.get("mile-disclosure")
        drive = request.form.get("drive")
        transmission = request.form.get("transmission")
        conditions = request.form.get("conditions")
        accident = request.form.get("accident")
        mechanical_issue = request.form.getlist("mechanical-issue")
        input_other = request.form.get("input-other")
        if "Other issues" in mechanical_issue:
            mechanical_issue[-1] += ': ' + input_other
        engine_issues = request.form.get("engine-issues")
        engine = request.form.get("engine")
        transmission_issues = request.form.get("transmission-issues")
        input_transmission = request.form.get("input-transmission")
        paint_issues = request.form.get("paint-issues")
        input_paint = request.form.get("input-paint")
        warning_lights_issues = request.form.get("warningLights-issues")
        input_warning_lights = request.form.get("input-warningLights")
        input_warningLights_other = request.form.get("input-warningLights-other")
        rust_issues = request.form.get("rust-issues")
        input_rust = request.form.get("input-rust")
        interior_issues = request.form.get("interior-issues")
        input_interior = request.form.get("input-interior")
        interior_parts_issues = request.form.get("interior-parts-issues")
        input_interior_parts = request.form.get("input-interior-parts")
        lift = request.form.get("lift")
        engine_modifications = request.form.get("engine-modifications")
        tires_issues = request.form.get("tires-issues")
        input_tires = request.form.get("input-tires")

        # Update the session["form_data"] dictionary with new form data
        session["form_data"]["input-mile"] = input_mile
        session["form_data"]["mile_disclosure"] = mile_disclosure
        session["form_data"]["drive"] = drive
        session["form_data"]["transmission"] = transmission
        session["form_data"]["conditions"] = conditions
        session["form_data"]["accident"] = accident
        session["form_data"]["mechanical-issue"] = mechanical_issue
        session["form_data"]["input-other"] = input_other
        session["form_data"]["engine-issues"] = engine_issues
        session["form_data"]["engine"] = engine
        session["form_data"]["transmission-issues"] = transmission_issues
        session["form_data"]["input-transmission"] = input_transmission
        session["form_data"]["paint-issues"] = paint_issues
        session["form_data"]["input-paint"] = input_paint
        session["form_data"]["warningLights-issues"] = warning_lights_issues
        session["form_data"]["input-warningLights-other"] = input_warningLights_other
        session["form_data"]["input-warningLights"] = input_warning_lights
        session["form_data"]["rust-issues"] = rust_issues
        session["form_data"]["input-rust"] = input_rust
        session["form_data"]["interior-issues"] = interior_issues
        session["form_data"]["input-interior"] = input_interior
        session["form_data"]["interior-parts-issues"] = interior_parts_issues
        session["form_data"]["input-interior-parts"] = input_interior_parts
        session["form_data"]["lift"] = lift
        session["form_data"]["engine-modifications"] = engine_modifications
        session["form_data"]["tires-issues"] = tires_issues
        session["form_data"]["input-tires"] = input_tires

        # Update the session object
        session.modified = True

        # Print the retrieved data to the console
        print("Vin:", vin)
        print("Input Mile:", input_mile)
        print("Mile Disclosure:", mile_disclosure)
        print("Drive:", drive)
        print("Transmission:", transmission)
        print("Conditions:", conditions)
        print("Accident:", accident)

        print("mechanical-issue: ", mechanical_issue)
        print("Input Other: ", input_other)

        print("Engine Issues:", engine_issues)
        print("Engine:", engine)
        print("Transmission Issues:", transmission_issues)
        print("Input Transmission:", input_transmission)
        print("Paint Issues:", paint_issues)
        print("Input Paint:", input_paint)
        print("Warning Lights Issues:", warning_lights_issues)
        print("Input Warning Lights:", input_warning_lights)
        print("Input Warning Lights:", input_warningLights_other)
        print("Rust Issues:", rust_issues)
        print("Input Rust:", input_rust)
        print("Interior Parts Issues:", interior_parts_issues)
        print("Input Interior Parts:", input_interior_parts)
        print("Lift:", lift)
        print("Engine Modifications:", engine_modifications)
        print("Tires-issues:", tires_issues)
        print("Input Tires:", input_tires)

        if vin != '':
            utils.update_google_sheet('Form Responses 1',
                                      [input_mile, mile_disclosure, utils.drive_full_name(drive),
                                       utils.transmission_full_name(transmission),
                                       utils.condition_full_name(conditions), accident,
                                       ";".join(mechanical_issue),
                                       "No" if engine == 'No' else utils.engine_issues_full_name(engine_issues),
                                       "No" if transmission_issues == 'No' else utils.transmission_issues_full_name(
                                           input_transmission),
                                       "No" if paint_issues == 'No' else utils.how_many_full_name(input_paint),
                                       "No" if warning_lights_issues == 'No' else utils.warning_lights_full_name(
                                           input_warning_lights, input_warningLights_other),
                                       "No" if rust_issues == 'No' else utils.rust_full_name(input_rust),
                                       "No" if interior_issues == 'No' else utils.how_many_full_name(input_interior),
                                       lift, engine_modifications,
                                       "No" if interior_parts_issues == 'No' else utils.how_many_full_name(
                                           input_interior_parts),
                                       "No" if tires_issues == 'No' else utils.how_many_full_name(input_tires)],
                                      ['J', 'Z'], vin)

        return redirect(url_for('index.image', vin=vin))


@index_bp.route('/image/<string:vin>', methods=["GET", "POST"])
def image(vin):
    if request.method == "GET":
        image_folder_path = os.path.join("static", "images", vin)
        try:
            session["form_data"]
        except:
            session["form_data"] = {}

        if os.path.exists('static/images/' + vin):
            for element in ALLOWED_ELEMENTS:
                element_path = os.path.join(image_folder_path, element)
                valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.PNG', '.JPG', '.JPEG', '.GIF']
                for ext in valid_extensions:
                    if os.path.exists(element_path + ext):
                        session["form_data"][element] = 'images/' + vin + '/' + element + ext
                        break
                else:
                    session["form_data"][element] = ''
        session.modified = True
        form_data = session.get("form_data", {})
        print(form_data)
        return render_template('image.html', form_data=form_data, vin=vin)
    else:
        current_drive_url, current_drive_id = utils.create_folder_if_not_exists('1EvYbjuCWqkww_TDOVMHHTiew2kVmQ02G',
                                                                                vin)
        utils.update_google_sheet('Form Responses 1', [current_drive_url], ['AA', 'AA'], vin)
        utils.update_google_sheet('Form Responses 1', ['http://chat4s.com/image/' + vin], ['AB', 'AB'], vin)
        utils.update_google_sheet('Form Responses 1', ['http://chat4s.com/make_offer/' + vin], ['AC', 'AC'], vin)
        for element in ALLOWED_ELEMENTS:
            try:
                uploaded_file = request.files.get(element)
                if uploaded_file:
                    original_filename = uploaded_file.filename
                    filename, file_extension = os.path.splitext(original_filename)

                    # Save the uploaded image to the appropriate directory
                    filename = f"{element}{file_extension}"
                    image_path = 'images/' + str(vin)
                    os.makedirs('static/' + image_path, exist_ok=True)
                    # Delete all files with matching prefix
                    for file in os.listdir('static/' + image_path):
                        if file.startswith(element):
                            os.remove(os.path.join('static/' + image_path, file))

                    uploaded_file.save('static/' + image_path + '/' + filename)
                    utils.upload_image_to_drive(element, 'static/' + image_path + '/' + filename, current_drive_id)

                    # Update the form data with the uploaded image filename
                    # Assuming you have a dictionary to store image filenames for each element
                    try:
                        session["form_data"][element] = image_path + '/' + filename
                        session.modified = True
                    except:
                        pass
            except:
                pass
        if 'image-all' in request.form:
            return redirect(url_for('index.complete', vin=vin))
        form_data = session.get("form_data", {})
        return redirect(url_for('index.image', form_data=form_data, vin=vin))


@index_bp.route('/extra_image/<string:vin>', methods=["GET", "POST"])
def extra_image(vin):
    if request.method == "GET":
        image_folder_path = os.path.join("static", "images", vin)
        try:
            session["form_data"]
        except:
            session["form_data"] = {}

        if os.path.exists('static/images/' + vin):
            for element in ALLOWED_ELEMENTS:
                element_path = os.path.join(image_folder_path, element)
                valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.PNG', '.JPG', '.JPEG', '.GIF']
                for ext in valid_extensions:
                    if os.path.exists(element_path + ext):
                        session["form_data"][element] = 'images/' + vin + '/' + element + ext
                        break
                else:
                    session["form_data"][element] = ''
        session.modified = True
        form_data = session.get("form_data", {})
        print(form_data)
        return render_template('extra_image.html', form_data=form_data, vin=vin)
    else:
        current_drive_url, current_drive_id = utils.create_folder_if_not_exists('1EvYbjuCWqkww_TDOVMHHTiew2kVmQ02G',
                                                                                vin)
        utils.update_google_sheet('Form Responses 1', [current_drive_url], ['AA', 'AA'], vin)
        utils.update_google_sheet('Form Responses 1', ['http://chat4s.com/image/' + vin], ['AB', 'AB'], vin)
        utils.update_google_sheet('Form Responses 1', ['http://chat4s.com/make_offer/' + vin], ['AC', 'AC'], vin)
        for element in ALLOWED_ELEMENTS:
            try:
                uploaded_file = request.files.get(element)
                if uploaded_file:
                    original_filename = uploaded_file.filename
                    filename, file_extension = os.path.splitext(original_filename)

                    # Save the uploaded image to the appropriate directory
                    filename = f"{element}{file_extension}"
                    image_path = 'images/' + str(vin)
                    os.makedirs('static/' + image_path, exist_ok=True)
                    # Delete all files with matching prefix
                    for file in os.listdir('static/' + image_path):
                        if file.startswith(element):
                            os.remove(os.path.join('static/' + image_path, file))

                    uploaded_file.save('static/' + image_path + '/' + filename)
                    utils.upload_image_to_drive(element, 'static/' + image_path + '/' + filename, current_drive_id)

                    # Update the form data with the uploaded image filename
                    # Assuming you have a dictionary to store image filenames for each element
                    try:
                        session["form_data"][element] = image_path + '/' + filename
                        session.modified = True
                    except:
                        pass
            except:
                pass
        if 'image-all' in request.form:
            return redirect(url_for('index.complete', vin=vin))
        form_data = session.get("form_data", {})
        return redirect(url_for('index.image', form_data=form_data, vin=vin))


@index_bp.route('/complete/<string:vin>', methods=["GET"])
def complete(vin):
    return render_template('complete.html', vin=vin)


@index_bp.route('/make_offer/<string:vin>', methods=["GET"])
def make_offer(vin):
    info = utils.get_info_from_sheet('Form Responses 1', vin)
    all_cols = utils.get_col_from_sheet('Form Responses 1')
    offer_status = all_cols.index('Maxoffer Status')
    if info[offer_status] == 'Pending' or '$' in info[offer_status]:
        return render_template('make_offer_repeat.html', vin=vin)
    return render_template('make_offer.html', vin=vin)


@index_bp.route('/make_offer_async/<string:vin>', methods=["POST"])
def make_offer_async(vin):
    info = utils.get_info_from_sheet('Form Responses 1', vin)
    all_cols = utils.get_col_from_sheet('Form Responses 1')
    offer_status = all_cols.index('Maxoffer Status')
    # update redeem offer
    carmax.get_redeem_offer(vin)
    if info[offer_status] == 'Pending' or '$' in info[offer_status]:
        carmax.get_offer()
        return '已更新'
    else:
        carmax.get_offer()
        current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        utils.update_google_sheet('Form Responses 1', ['Pending', current_time], ['AE', 'AF'], vin)
        result = carmax.submit_form(vin)
        utils.update_google_sheet('Form Responses 1', [result, current_time], ['AE', 'AF'], vin)
        return '已提交'
