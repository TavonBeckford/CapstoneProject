"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from app.LicencePlateExtractor import *
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, g, _request_ctx_stack
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import *
from app.models import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask.json import jsonify
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import jwt
import random
from sqlalchemy import and_
from functools import wraps
from flask.helpers import send_from_directory
from app import mail
from flask_mail import Message


USR_DATE_FORMAT = "%b %d, %Y"
SYS_DATE_FORMAT = "%Y-%m-%d"
USR_TIME_FORMAT = "%I:%M %p"
SYS_TIME_FORMAT = "%H:%M:%S"
USR_DATETIME_FORMAT = f"{USR_DATE_FORMAT} {USR_TIME_FORMAT}"
SYS_DATETIME_FORMAT = f"{SYS_DATE_FORMAT} {SYS_TIME_FORMAT}"


# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

###
# Routing for the application.
###

@app.route("/api/register", methods=["POST"])
def register():
    """ Register a user """
    # if current_user.is_authenticated:
    #     return redirect(url_for('secure_page'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # include security checks #
        username = request.form['username']
        password = request.form['password']
        isAdmin = request.form['isAdmin']

        if User.query.filter_by(username=username).first(): # if username already exist
            response = jsonify({'error':'Try a different username or contact the administrator.'})
            return response

        user = User(isAdmin, username, password, SaltGenerator.string(64))

        db.session.add(user)
        db.session.commit()

        # convert sqlalchemy user object to dictionary object for JSON parsing
        data = obj_to_dict(user)
        data.pop('password')
        response = jsonify(data)
        return response
    else:
        response = jsonify(form.errors)
        return response


@app.route("/api/auth/login", methods=["POST"])
def login():
    """ Login a user """
    # if current_user.is_authenticated:
    #     return redirect(url_for('secure_page'))
    form = LoginForm()
    if form.validate_on_submit():
        # include security checks #
        username = request.form['username']
        password = request.form['password']

        # db access
        user = User.query.filter_by(username=username).first()
        # validate the password and ensure that a user was found
        if user is not None and check_password_hash(user.password, password + user.salt):
            login_user(user)
            payload = {
                "sub": "352741018090",
                "name": username,
                "issue": current_datetime(SYS_DATETIME_FORMAT)
            }
            encoded_jwt = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            response = jsonify({"message": "Login Successful", 'token':encoded_jwt, 'user':{'id':user.id, 'name':user.username}}) # Hash user_id before sending
            return response
        else:
            response = jsonify({'error':'Username or Password is incorrect.'})
            return response
    else:
        response = jsonify(form.errors)
        return response


@app.route("/api/auth/logout", methods=["POST"])
@requires_auth
def logout():
    """Logs out the user and ends the session"""

    try:
        logout_user()
    except Exception:
        return 'Access token is missing or invalid, 401'

    response = jsonify({"message": "Log out successful"})
    return response


@app.route("/api/simulate", methods=["GET"])
@requires_auth
def simulateOffense():
    """ Simulate an Offense """


    ###----------- HELPER FUNCTIONS-----------##


    ###----------- END HELPER FUNCTIONS-----------##



    ###----------- START SIMULATION -----------##


    # SELECT A RANDOM OFFENCE, LOCATION AND IMAGE
    offence = get_random_record(Offence)
    location = get_random_record(Location)
    image = get_random_file(app.config['UPLOADS_FOLDER'])   # Return a random file from the uploads folder

    # IF THERE ARE NO MORE IMAGES IN THE ./uploads FOLDER
    # RETURN None

    if image == None:
        print('\nNO MORE IMAGES TO SERVE\n')
        return generate_empty_ticket()
    
    # IF THERE ARE NO Locations IN THE DB
    # RETURN BLANK None
    if location == None:
        print('\nNo locations found\n')
        return generate_empty_ticket()

    # IF THERE ARE NO Offences IN THE DB
    # RETURN None
    if offence == None:
        print('\nNo offences found\n')
        return generate_empty_ticket()
    
    incident = generateIncident(current_datetime(SYS_DATE_FORMAT), current_datetime(SYS_TIME_FORMAT), location, offence, image)
    
    if incident == None:
        return generate_empty_ticket()

    # Convert objects from query results to python dictionaries
    incidentObj = obj_to_dict(incident)
    offenceObj = obj_to_dict(offence)
    locationObj = obj_to_dict(location)

    registrationNumber = '-'
    ticketStatus = ''

    # Parse Image
    try:
        print(f'\nParsing Image: {image}\n')
        registrationNumber = parseImage(image)
        print(f'\nRegistrationNumber: {registrationNumber}\n')
    except Exception:
        ticketStatus = 'IMAGE PROCESSING ERROR'

    if ticketStatus == 'IMAGE PROCESSING ERROR':
        ticketData = IPEHandler(incidentObj, offenceObj, locationObj, ticketStatus)
        return ticketData
    else:

        print(f"\nGETTING VEHICLE & VEHICLE OWNER FROM DB")
        # Get Vehicle & Vehicle Owner
        owner = VehicleOwner.query.filter_by(licenseplate=registrationNumber).first()
        print('\nOwner',owner)
        vehicle = Vehicle.query.filter_by(licenseplate=registrationNumber).first()

        # RUN EXCEPTION HANDLER IF Registration # was incorrectly identified
        if owner == None or vehicle == None:
            ticketStatus = 'IMAGE PROCESSING ERROR'
            print(f"\nNO VEHICLE OR VEHICLE OWNER FOUND")
            ticketData = IPEHandler(incidentObj, offenceObj, locationObj, ticketStatus)
            return ticketData

        ownerObj = obj_to_dict(owner)
        vehicleObj = obj_to_dict(vehicle)

        print(f"\nFORMATTING DATA FOR SENDING")
        # Format dates, fine and image path for frontend
        ownerObj['expdate'] = str(ownerObj['expdate'].strftime(USR_DATE_FORMAT))
        vehicleObj['expdate'] = str(vehicleObj['expdate'].strftime(USR_DATE_FORMAT))
        ownerObj['dob'] = str(ownerObj['dob'].strftime(USR_DATE_FORMAT))
        incidentObj['date'] = str(incidentObj['date'].strftime(USR_DATE_FORMAT))
        incidentObj['time'] = str(incidentObj['time'].strftime(USR_TIME_FORMAT))
        imgName = incidentObj['image']
        offenceObj['fine'] = trioFormatter(offenceObj['fine'])

        ticket = None
        imgPath = ''

        # CHECK TO SEE WHETHER OR NOT THE VEHICLE OWNER HAS AN EMAIL ADDRESS ON FILE
        emailAddress = ownerObj['email']
        if emailAddress != '':
            #sendEmail(f'http://localhost:8080/issued/{registrationNumber}_{imgName}',[emailAddress])
            ticketStatus = f"ISSUED VIA ({emailAddress})"
            print(f"\nTICKET STATUS: {ticketStatus}")
            # Create the Ticket and save to JETS' Database/Ticket table
            # Ticket status will determine whether or not the ticket will apprear under the notifications table
            print(f"\nCREATING AN ISSUED TICKET FOR DATABASE")
            ticket = IssuedTicket(ownerObj['trn'], incidentObj['id'], datetime.now(), ticketStatus)
            print(f"\nTICKET OBJECT CREATED")
            # SET NEW FILE PATH TO ./uploads/issued
            imgPath = os.path.join(app.config['ISSUED_FOLDER'], imgName)
        else:
            ticketStatus = 'NO EMAIL ADDRESS ON FILE'
            print(f"\nTICKET STATUS: {ticketStatus}")
            print(f"\nCREATING A FLAGGED EMAIL TICKET FOR DATABASE")
            # Create the Ticket and save to JETS' Database/Ticket table
            # Ticket status will determine whether or not the ticket will apprear under the notifications table 
            ticket = FlaggedEmail(ownerObj['trn'], incidentObj['id'], datetime.now(), ticketStatus)
            # SET NEW FILE PATH TO ./uploads/flagged
            imgPath = os.path.join(app.config['FLAGGED_FOLDER'], imgName)

        print(f"\nCOMMITTING TICKET TO DB")
        db_commit(ticket)
        db.session.refresh(ticket)

        #ASSIGN FILE PATH & MOVE FILE FROM ./uploads to ./imgpath
        incidentObj['image'] = imgPath
        os.rename(os.path.join(app.config['UPLOADS_FOLDER'], imgName),imgPath)

        # FORMAT DATE ISSUED
        dateIssued = str(ticket.datetime.strftime(USR_DATETIME_FORMAT))

        ticketData = {
            'vehicleOwner': ownerObj,
            'vehicle': vehicleObj,
            'offence': offenceObj,
            'incident': incidentObj,
            'location': locationObj,
            'status': ticket.status,
            'dateIssued': dateIssued,
            'id': ticket.id
        }
        print(f"\nSENDING DATA TO VIEW...\n")
        return jsonify(ticketData)

###----------- END SIMULATION -----------##

@app.route("/api/issued", methods=["GET"])
@requires_auth
def getIssuedTickets():
    """ Get a list of all issued traffic tickets """

    ticketObjs = []
    tickets = db.session.query(IssuedTicket).all()
    if tickets == []:
        print(f'\nNO ISSUED TICKET, SENDING: {tickets}')
        return jsonify(ticketObjs)

    for ticket in tickets:
        ticketID = ticket.id
        ticketData = getIssuedTicket(ticketID).get_json()    #json response to python dict
        ticketObjs.append(ticketData)
    response = jsonify(ticketObjs)
    return response


@app.route("/api/flagged", methods=["GET"])
@requires_auth
def getFlaggedTickets():
    """ Get a list of all flagged traffic tickets """

    ticketObjs = []
    tickets = db.session.query(FlaggedEmail).all()
    tickets.extend(db.session.query(FlaggedImage).all())
    if tickets == None:
        return jsonify(ticketObjs)

    for ticket in tickets:
        ticketID = ticket.id
        ticketStatus = ticket.status
        ticketData = getFlaggedTicket(ticketID,ticketStatus).get_json()    #json response to python dict
        ticketObjs.append(ticketData)
    response = jsonify(ticketObjs)
    return response


@app.route("/api/issued/<ticketID>", methods=["GET"])
@requires_auth
def getIssuedTicket(ticketID):
    """ Get a successfully issued traffic ticket """

    ticket = IssuedTicket.query.get(ticketID)
    if ticket == None:
        print('\nTICKET NOT FOUND\n')
        return jsonify({})

    incident = Incident.query.get(ticket.incidentID)
    offence  = Offence.query.get(incident.offenceID)
    location = Location.query.get(incident.locationID)
    owner = VehicleOwner.query.filter_by(trn=ticket.trn).first()
    vehicle = Vehicle.query.filter_by(licenseplate=owner.licenseplate).first()

    # Convert database objects to python dictionaries
    incidentObj = obj_to_dict(incident)
    offenceObj = obj_to_dict(offence)
    locationObj = obj_to_dict(location)
    ownerObj = generateNullVehicleOwner()
    vehicleObj = generateNullVehicle()
    ownerObj = obj_to_dict(owner)
    vehicleObj = obj_to_dict(vehicle)

    # Format data before sending
    ownerObj['expdate'] = str(ownerObj['expdate'].strftime(USR_DATE_FORMAT))
    vehicleObj['expdate'] = str(vehicleObj['expdate'].strftime(USR_DATE_FORMAT))
    ownerObj['dob'] = str(ownerObj['dob'].strftime(USR_DATE_FORMAT))
    ownerObj['trn'] = trioFormatter(ownerObj['trn'], ' ')

    # Format data before sending
    incidentObj['paymentDeadline'] = str((incidentObj['date'] + timedelta(60)).strftime(USR_DATE_FORMAT))
    incidentObj['date'] = str(incidentObj['date'].strftime(USR_DATE_FORMAT))
    incidentObj['time'] = str(incidentObj['time'].strftime(USR_TIME_FORMAT))
    incidentObj['image'] = os.path.join(app.config['ISSUED_FOLDER'], incidentObj['image'])[1:]
    offenceObj['fine'] = trioFormatter(offenceObj['fine'])
    
    # FORMAT DATE ISSUED
    dateIssued = str(ticket.datetime.strftime(USR_DATETIME_FORMAT))

    return jsonify({
        'vehicleOwner': ownerObj,
        'vehicle': vehicleObj,
        'offence': offenceObj,
        'incident': incidentObj,
        'location': locationObj,
        'dateIssued': dateIssued,
        'status': ticket.status,
        'id': str(ticket.id).zfill(9)
    })


@app.route("/api/flagged/<int:ticketID>/<ticketStatus>", methods=["GET"])
@requires_auth
def getFlaggedTicket(ticketID, ticketStatus):
    """ Get a successfully issued traffic ticket """

    ticket = {}

    ownerObj = generateNullVehicleOwner()
    vehicleObj = generateNullVehicle()

    if ticketStatus == 'IMAGE PROCESSING ERROR':
        ticket = FlaggedImage.query.get(ticketID)
        if ticket == None:
            print('\nTICKET NOT FOUND\n')
            return jsonify({})

    if ticketStatus == 'NO EMAIL ADDRESS ON FILE':
        ticket = FlaggedEmail.query.get(ticketID)
        owner = VehicleOwner.query.filter_by(trn=ticket.trn).first()
        vehicle = Vehicle.query.filter_by(licenseplate=owner.licenseplate).first()
        ownerObj = obj_to_dict(owner)
        vehicleObj = obj_to_dict(vehicle)

        # Format data before sending
        ownerObj['expdate'] = str(ownerObj['expdate'].strftime(USR_DATE_FORMAT))
        vehicleObj['expdate'] = str(vehicleObj['expdate'].strftime(USR_DATE_FORMAT))
        ownerObj['dob'] = str(ownerObj['dob'].strftime(USR_DATE_FORMAT))
        ownerObj['trn'] = trioFormatter(ownerObj['trn'], ' ')

        if ticket == None:
            print('\nTICKET NOT FOUND\n')
            return jsonify({})
    
    incident = Incident.query.get(ticket.incidentID)
    offence  = Offence.query.get(incident.offenceID)
    location = Location.query.get(incident.locationID)

    # Convert database objects to python dictionaries
    incidentObj = obj_to_dict(incident)
    offenceObj = obj_to_dict(offence)
    locationObj = obj_to_dict(location)
    
    # Format data before sending
    incidentObj['paymentDeadline'] = '-'
    incidentObj['date'] = str(incidentObj['date'].strftime(USR_DATE_FORMAT))
    incidentObj['time'] = str(incidentObj['time'].strftime(USR_TIME_FORMAT))
    incidentObj['image'] = os.path.join(app.config['FLAGGED_FOLDER'], incidentObj['image'])[1:]
    offenceObj['fine'] = trioFormatter(offenceObj['fine'])
        
    return jsonify({
        'vehicleOwner': ownerObj,
        'vehicle': vehicleObj,
        'offence': offenceObj,
        'incident': incidentObj,
        'location': locationObj,
        'dateIssued': '-',
        'status': ticket.status,
        'id': str(ticket.id).zfill(9)
    })


@app.route("/api/issue", methods=["POST"])
@requires_auth
def issueTicket():
    """ Add a new offender """

    form = IssueTicketForm()    # TICKET containing all ticket-related data; vehicleowner, vehicle, traffic cam, tax authority

    print('\nReceived Issue Ticket Form')

    if form.validate_on_submit():
        print('\nForm has been validated')
        # include security checks #


        # INCIDENT INFORMATION
        date = request.form['date'].split('/')
        date = datetime(int(date[0]), int(date[1]), int(date[2])).strftime(SYS_DATE_FORMAT)
        print('\nDate:', date)
        time = request.form['time']
        time = f'{time}:00'
        print('\nTime:', time)

        location = request.form['location']
        parish = request.form['parish']

        dbLocation = Location.query.filter_by(description=location).first()
        print('\nFetched Location in DB:', dbLocation)
        if dbLocation is None:
            print('\nCreating new Location in DB')
            location = Location(location, parish)
            db_commit(location)
            db.session.refresh(location)
        else:
            location = dbLocation
        

        offenceCode = request.form['offence']
        offence = Offence.query.filter_by(code=offenceCode).first()


        licensePlateImage = request.files['snapshot']
        imageName = secure_filename(licensePlateImage.filename)
        print('\nSaving image file to uploads dir')
        licensePlateImage.save(os.path.join(app.config['UPLOADS_FOLDER'], imageName))

        # IF THERE ARE NO MORE IMAGES IN THE ./uploads FOLDER
        # RETURN None

        if imageName == None:
            print('\nNO MORE IMAGES TO SERVE\n')
            return generate_empty_ticket()
        
        # IF THERE ARE NO Locations IN THE DB
        # RETURN BLANK None
        if location == None:
            print('\nNo locations found\n')
            return generate_empty_ticket()

        # IF THERE ARE NO Offences IN THE DB
        # RETURN None
        if offence == None:
            print('\nNo offences found\n')
            return generate_empty_ticket()
        
        incident = generateIncident(date, time, location, offence, imageName)
        
        if incident == None:
            return generate_empty_ticket()

        # Convert objects from query results to python dictionaries
        incidentObj = obj_to_dict(incident)
        offenceObj = obj_to_dict(offence)
        locationObj = obj_to_dict(location)

        registrationNumber = '-'
        ticketStatus = ''

        # Parse Image
        try:
            print(f'\nParsing Image: {imageName}\n')
            registrationNumber = parseImage(imageName)
            print(f'\nRegistrationNumber: {registrationNumber}\n')
        except Exception:
            ticketStatus = 'IMAGE PROCESSING ERROR'

        if ticketStatus == 'IMAGE PROCESSING ERROR':
            ticketData = IPEHandler(incidentObj, offenceObj, locationObj, ticketStatus)
            return ticketData
        else:

            print(f"\nGETTING VEHICLE & VEHICLE OWNER FROM DB")
            # Get Vehicle & Vehicle Owner
            owner = VehicleOwner.query.filter_by(licenseplate=registrationNumber).first()
            print('\nOwner',owner)
            vehicle = Vehicle.query.filter_by(licenseplate=registrationNumber).first()

            # RUN EXCEPTION HANDLER IF Registration # was incorrectly identified
            if owner == None or vehicle == None:
                ticketStatus = 'IMAGE PROCESSING ERROR'
                print(f"\nNO VEHICLE OR VEHICLE OWNER FOUND")
                ticketData = IPEHandler(incidentObj, offenceObj, locationObj, ticketStatus)
                return ticketData

            ownerObj = obj_to_dict(owner)
            vehicleObj = obj_to_dict(vehicle)

            print(f"\nFORMATTING DATA FOR SENDING")
            # Format dates, fine and image path for frontend
            ownerObj['expdate'] = str(ownerObj['expdate'].strftime(USR_DATE_FORMAT))
            vehicleObj['expdate'] = str(vehicleObj['expdate'].strftime(USR_DATE_FORMAT))
            ownerObj['dob'] = str(ownerObj['dob'].strftime(USR_DATE_FORMAT))
            incidentObj['date'] = str(incidentObj['date'].strftime(USR_DATE_FORMAT))
            incidentObj['time'] = str(incidentObj['time'].strftime(USR_TIME_FORMAT))
            imgName = incidentObj['image']
            offenceObj['fine'] = trioFormatter(offenceObj['fine'])

            ticket = None
            imgPath = ''

            # CHECK TO SEE WHETHER OR NOT THE VEHICLE OWNER HAS AN EMAIL ADDRESS ON FILE
            emailAddress = ownerObj['email']
            if emailAddress != '':
                #sendEmail(f'http://localhost:8080/issued/{registrationNumber}_{imgName}',[emailAddress])
                ticketStatus = f"ISSUED VIA ({emailAddress})"
                print(f"\nTICKET STATUS: {ticketStatus}")
                # Create the Ticket and save to JETS' Database/Ticket table
                # Ticket status will determine whether or not the ticket will apprear under the notifications table
                print(f"\nCREATING AN ISSUED TICKET FOR DATABASE")
                ticket = IssuedTicket(ownerObj['trn'], incidentObj['id'], datetime.now(), ticketStatus)
                print(f"\nTICKET OBJECT CREATED")
                # SET NEW FILE PATH TO ./uploads/issued
                imgPath = os.path.join(app.config['ISSUED_FOLDER'], imgName)
            else:
                ticketStatus = 'NO EMAIL ADDRESS ON FILE'
                print(f"\nTICKET STATUS: {ticketStatus}")
                print(f"\nCREATING A FLAGGED EMAIL TICKET FOR DATABASE")
                # Create the Ticket and save to JETS' Database/Ticket table
                # Ticket status will determine whether or not the ticket will apprear under the notifications table 
                ticket = FlaggedEmail(ownerObj['trn'], incidentObj['id'], datetime.now(), ticketStatus)
                # SET NEW FILE PATH TO ./uploads/flagged
                imgPath = os.path.join(app.config['FLAGGED_FOLDER'], imgName)

            print(f"\nCOMMITTING TICKET TO DB")
            db_commit(ticket)
            db.session.refresh(ticket)

            #ASSIGN FILE PATH & MOVE FILE FROM ./uploads to ./imgpath
            incidentObj['image'] = imgPath
            os.rename(os.path.join(app.config['UPLOADS_FOLDER'], imgName),imgPath)

            # FORMAT DATE ISSUED
            dateIssued = str(ticket.datetime.strftime(USR_DATETIME_FORMAT))

            ticketData = {
                'vehicleOwner': ownerObj,
                'vehicle': vehicleObj,
                'offence': offenceObj,
                'incident': incidentObj,
                'location': locationObj,
                'status': ticket.status,
                'dateIssued': dateIssued,
                'id': ticket.id
            }
            print(f"\nSENDING DATA TO VIEW...\n")
            return jsonify(ticketData)
    print('\nForm not validated')
    print(form.errors)
    return generate_empty_ticket()


@app.route("/api/search/tickets", methods=["GET"])
# @requires_auth
def searchTickets():
    """ Search for offenders based on their name, date of offence or ticket status """

    q = request.args.get('q')
    print('\nQuery:', q)

    tickets = []

    results = IssuedTicket.query.filter_by(trn=q).all()
    tickets.extend(results)

    results = FlaggedEmail.query.filter_by(trn=q).all()
    tickets.extend(results)

    # Return all issued tickets where Vehicle registration number is <q>
    subquery = db.session.query(VehicleOwner.trn).filter(VehicleOwner.licenseplate==q).subquery() # Get trn using reg #
    results = db.session.query(IssuedTicket).filter(IssuedTicket.trn.in_(subquery)) # Get tickets using trn from subquery
    tickets.extend(results)

    ticketObjs = []
    for ticket in tickets:
        ticketID = ticket.id
        ticketStatus = ticket.status
        if ticketStatus.startswith('ISSUED'):
            ticketData = getIssuedTicket(ticketID).get_json()    #json response to python dict
        else:
            ticketData = getFlaggedTicket(ticketID, ticketStatus).get_json()    #json response to python dict
        
        ticketObjs.append(ticketData)
    
    response = jsonify(ticketObjs)

    # ticketData = {
    #     'vehicleOwner': ownerObj,
    #     'vehicle': vehicleObj,
    #     'offence': offenceObj,
    #     'incident': incidentObj,
    #     'location': locationObj,
    #     'status': ticket.status,
    #     'dateIssued': dateIssued,
    #     'id': ticket.id
    # }
    
    print('\nSearch Results:', response)
    return response


@app.route("/api/users/<int:user_id>", methods=["GET"])
@login_required
def getUser(user_id):
    """ Get details for a specific user """
    if str(user_id) != current_user.get_id():
        return jsonify(message="Invalid Request")

    user = User.query.get(user_id)
    if user is None:
        return jsonify(message="User not found")
    
    user = obj_to_dict(user)
    user.pop('password')
    return jsonify(user)


@app.route('/uploads/<filename>')
def get_new_upload(filename):
    print('GETTING FILE FROM UPLOADS_FOLDER')
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOADS_FOLDER']),filename)

@app.route('/uploads/issued/<filename>')
def get_issued_upload(filename):
    print('GETTING FILE FROM ISSUED_FOLDER')
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['ISSUED_FOLDER']),filename)

@app.route('/uploads/flagged/<filename>')
def get_flagged_upload(filename):
    print('GETTING FILE FROM FLAGGED_FOLDER')
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['FLAGGED_FOLDER']),filename)


########## --------- HELPER FUNCTIONS --------- ###########

@app.route('/api/resetSimulation', methods=["GET"])
@requires_auth
def resetSimulation():
    print('\nRESETTING SIMULATION')
    try:
        reset_uploads_dir()
        print('\nClearing DB tables'.upper())
        clear_db_table(IssuedTicket)
        clear_db_table(FlaggedImage)
        clear_db_table(FlaggedEmail)
        clear_db_table(Incident)
        print('\n')
        return jsonify({'message':'Simulation data has been reset'})
    except Exception as e:
        print(e)
        return jsonify({'message':'An error occurred while resetting simulation'})

def reset_uploads_dir():
    '''Move flagged and issued files to uploads directory'''

    flagged = app.config['FLAGGED_FOLDER']
    issued = app.config['ISSUED_FOLDER']
    uploads = app.config['UPLOADS_FOLDER']

    files = getFilenames(flagged)
    if files != []:
        print('\nMoving files from flagged folder to uploads folder')
        # Move files from flagged folder to uploads folder
        for file in files:
            print(f'\t{file}')
            os.rename(os.path.join(flagged, file), os.path.join(uploads, file))
    else:
        print(f'\nFlagged folder is empty!')  

    files = getFilenames(issued)
    if files != []:
        print('\nMoving files from issued folder to uploads folder')
        # Move files from issued folder to uploads folder
        for file in getFilenames(issued):
            print(f'\t{file}')
            os.rename(os.path.join(issued, file), os.path.join(uploads, file))
        print('\nMoved files from issued folder to uploads folder')
    else:
        print(f'\nIssued folder is empty!')  

def clear_db_table(table):
    results = db.session.query(table).all()
    if results != []:
        print('\n\tClearing DB table:', table)
        for result in results:
            print(f'\t{result}')
            db.session.delete(result)
            db.session.commit()
    else:
        print(f'\tTable {table} is empty!')  


def getFilenames(path):
    '''Returns a list of filenames within the given file path'''

    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
        return files

def get_random_file(path):
    '''Returns a randomly selected filename from the given file path'''
    '''Returns None if the directory is empty'''

    images = getFilenames(path)

    if images == []:
        return None
    return random.choice(images)

def get_random_record(db_table):
    '''Returns a randomly selected record from the given table'''
    '''Returns None if the table is empty'''

    records  = db.session.query(db_table).all() # List of records within the given table
    if records == []:
        return None
    return random.choice(records)  # Return a random choice


def generate_empty_ticket():
    '''Returns Ticket attributes with empty values'''

    return {
            'vehicleOwner': '',
            'vehicle': '',
            'offence': '',
            'incident': '',
            'location': '',
            'status': '',
            'dateFlagged': '',
            'id': '#'
        }

def db_commit(record):
    '''Commits the given record to the DB'''
    print('Saving record to db')
    db.session.add(record)
    db.session.commit()

# FOR GENERATING AND SAVING AN INCIDENT TO THE DB
def generateIncident(date, time, location, offence, image):
    '''Stores and Returns a new Incident having the given fields'''
   
    try:
        print('\nGenerating new Incident')
        # CREATE A NEW INCIDENT
        incident = Incident(date, time, location.id, offence.code, image)

        # SAVE NEW INCIDENT TO DB
        db_commit(incident)

        return incident
    except Exception:
        print('\nAn exception occurred!\n')
        return None

def sendEmail(message, recipients, offence=''):
    # Prepare and send email
    msg = Message('Committing a Traffic Offence', sender=('JamaicaEye Ticketing System',
    'traffic.division@jcf.gov.jm'),recipients=recipients)
    msg.body = 'You are hereby charged for having committed the offence described within the e-ticket found at:\n\n'
    msg.body += message + '\n\n'
    msg.body += 'You may optionally print this traffic ticket using your web browser\'s native print function.\n\n'
    msg.body += 'Should you have any queries, kindly direct them to jets.queries@jcf.gov.jm.\n'
    mail.send(msg)
    print('\nEmail has been delivered to:', recipients[0],'\n')


def parseImage(image):
    registrationNumber = LPDetector(image)
    registrationNumber = ''.join(e for e in registrationNumber if e.isalnum())
    return registrationNumber


# For handling IMAGE PROCESSING EXCEPTIONS (IPE)
def IPEHandler(incidentObj, offenceObj, locationObj, ticketStatus):
    print("\nRUNNING EXCEPTION HANDLER")
    # Generate a Vehicle and a Vehicle Owner with empty attribute values
    vehicleObj = generateNullVehicle()
    ownerObj = generateNullVehicleOwner()

    # Format dates, fine and image path for frontend
    incidentObj['date'] = str(incidentObj['date'].strftime(USR_DATE_FORMAT))
    incidentObj['time'] = str(incidentObj['time'].strftime(USR_TIME_FORMAT))
    offenceObj['fine'] = trioFormatter(offenceObj['fine'])
    imgName = incidentObj['image']

    # Create a 'FLAGGED IMAGE' Ticket and save to JETS' Database, ie. FlaggedImage table
    # Ticket status will determine whether or not the ticket will apprear under the notifications table
    print(f'\nTICKET STATUS: {ticketStatus}')
    ticket = FlaggedImage(incidentObj['id'], datetime.now(), ticketStatus)

    try:
        db_commit(ticket)
        db.session.refresh(ticket)
    except Exception:
        print(f'\nERROR SAVING FLAGGED IMAGE TO DB, MAYBE DUPLICATE INCIDENT ID')

    print(f'A FlaggedImage Ticket was added: {ticket}')

    # ASSIGN NEW FILE PATH & MOVE FILE
    incidentObj['image'] = os.path.join(app.config['FLAGGED_FOLDER'], imgName)
    os.rename(os.path.join(app.config['UPLOADS_FOLDER'], imgName),os.path.join(app.config['FLAGGED_FOLDER'], imgName))
    
    # FORMAT DATE FLAGGED
    dateFlagged = str(ticket.datetime.strftime(USR_DATETIME_FORMAT))
    
    ticketData = {
        'vehicleOwner': ownerObj,
        'vehicle': vehicleObj,
        'offence': offenceObj,
        'incident': incidentObj,
        'location': locationObj,
        'status': ticket.status,
        'dateFlagged': dateFlagged,
        'id': ticket.id
    }

    return jsonify(ticketData)


def generateNullVehicleOwner():
    # Generate a Vehicle Owner with empty attribute values
    return {
        'trn': '-',
        'fname': '-',
        'lname': ' ',
        'mname': '-',
        'address':'-',
        'country': '-',
        'parish': '-',
        'email':'-',
        'dob': '-',
        'gender':'-',
        'licenseplate': '-',
        'licensein': '-',
        'expdate': '-',
        'licenseType' :'-'
    }

def generateNullVehicle():
    # Generate a Vehicle with empty attribute values
    return {
        'licenseplate': '-',
        'make': '-',
        'model': '-',
        'colour' : '-',
        'year': '-',
        'licensediscno': '-',
        'cartype': '-',
        'expdate': '-'
    }

# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".

    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Flash errors from the form if validation fails with Flask-WTF
# http://flask.pocoo.org/snippets/12/
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            msg = f"Error in the {getattr(form, field).label.text} field - {error}"
            flash(msg, 'danger')
            


###
# Utilities
###

def current_datetime(format="%b %d, %Y %I:%M %p"):
    return datetime.now().strftime(format)

def obj_to_dict(obj):
    '''Converts an sqlalchemy database object to a dictionary format'''
    data = {}
    try:    # obj may not have an id property
        data = {'id':obj.get_id()}
    except Exception:
        pass
    parish= db.Column(db.String(30), nullable=False)
    email= db.Column(db.String(60), nullable=False)

    try:
        for k, v in obj.__dict__.items():
            if k != '_sa_instance_state':
                data[k] = v
    except Exception:
        pass

    return data

def trnFormatter(trn, sep=' '):
    trn = str(trn)
    new_trn = ''
    for i in range(len(trn)):
        new_trn += trn[i]
        if (i+1) % 3 == 0:
            new_trn += sep
    return new_trn

def trioFormatter(price, sep=','):
    '''Formats a number to include a thousandths separator'''
    price = str(price)
    pos = price.find('.') 
    if pos > 0:
        price = price[:pos]
    priceLength = len(price)
    commaPosition = priceLength % 3
    if commaPosition == 0:
        commaPosition += 3
    formattedPrice = ""  
    for i in range(0, priceLength):
        if i == commaPosition:
            formattedPrice += (sep)
            commaPosition += 3
        formattedPrice += price[i]
    return formattedPrice


# A function to populate the database with fake data
def populateDatabase():
    '''DATABASE INSERTS'''

    print('\nPOPULATING USER DB...\n')
    admin = User('Damion Lawson','admin','True')

    officer1 = User('Johanna Thompson-Whyte','password123')
    officer2 = User('Andrew Black','password123')

    db.session.add(admin)
    db.session.add(officer1)
    db.session.add(officer2)
    db.session.commit()
    print('\nUSER DB HAS BEEN POPULATED...\n')

    '''vehicle1 = Vehicle('9518JK', 'Toyota', 'Belta', 'White', 2009, 'JV390145', 'Sedan', '2022-07-11')
    vehicleOwner1 = VehicleOwner('234351389','Anne','Arden','Ramirez','58 Killarney Rd, Ocho Rios, St.Ann','St. Thomas','Jamaica','testable876@gmail.com','1985-5-21','Female','9518JK','Jamaica','2024-09-25','General')

    vehicle2 = Vehicle('8424GR','Toyota','Mark II Tourier','Silver',2003,'CJ128912','Sedan','2022-09-20')
    vehicleOwner2 = VehicleOwner('168858869','Michael','Nash','Rice','41 Angels Walks Rd, Spanish Town, St. Catherine','Portland','Jamaica','testable876@gmail.com','1991-10-11','Male','8424GR','Jamaica','2025-10-07','General')

    vehicle3 = Vehicle('DEPMED','Toyota','Prado','Silver',2006,'MK105873','SUV','2022-08-10')
    vehicleOwner3 = VehicleOwner('123077859','Edward','Isaiah','Winden','13 Mutex Ave, Maypen, Clarendon','St. Catherine','Jamaica','testable876@gmail.com','1983-07-15','Male','DEPMED','Jamaica','2023-01-09','General')

    vehicle4 = Vehicle('2445GX','Toyota','Carolla','Silver',2002,'AB781003','Sedan','2022-04-11')
    vehicleOwner4 = VehicleOwner('103975746','Navuna','Marcia','Evans','33 Watson Street, Mandeville, Manchester','Manchester','Jamaica','testable876@gmail.com','1989-12-15','Female','2445GX','Jamaica','2023-01-18','Private')

    vehicle5 = Vehicle('1206FQ','Toyota','Fortuner','Blue',2007,'RM125548','SUV','2022-06-11')
    vehicleOwner5 = VehicleOwner('281590140','Willesly','Jehory','Durant','4 Johns Ave, Molynes Rd, Kingston 11','St. Andrew','Jamaica','testable876@gmail.com','2000-11-11','Male','1206FQ','Jamaica','2022-05-14','Private')

    vehicle6 = Vehicle('6606HW','Toyota','Carolla','Black',1996,'KL323654','Sedan','2022-06-08')
    vehicleOwner6 = VehicleOwner('267041347','Venice','Anika','Salmon','28 Reeves Ave, Graham Rd, Kingston 12','St. Andrew','Jamaica','testable876@gmail.com','2001-10-18','Female','6606HW','Jamaica','2022-05-14','General')

    vehicle7 = Vehicle('3840GF','Toyota','Fielder','Black',2004,'LP830547','Sedan','2022-02-07')
    vehicleOwner7 = VehicleOwner('185671235','Kevin','Jamie','Bullock','28 West Minister Ave, Garnett Rd, Kingston 3','St. Andrew','Jamaica','testable876@gmail.com','1995-10-28','Male','3840GF','Jamaica','2024-08-19','General')

    vehicle8 = Vehicle('4737HA','Toyota','Prado','Silver',2013,'PT124785','SUV','2020-08-01')
    vehicleOwner8 = VehicleOwner('141158951','Carlton','Omar','Stevens','46 Walkers Dr, Orange Rd, Barbican','Kingston','Jamaica','testable876@gmail.com','1985-12-27','Male','4737HA','Jamaica','2024-08-29','General')


    db.session.add(vehicle1)
    db.session.add(vehicle2)
    db.session.add(vehicle3)
    db.session.add(vehicle4)
    db.session.add(vehicle5)
    db.session.add(vehicle6)
    db.session.add(vehicle7)
    db.session.add(vehicle8)

    db.session.commit()
    print('ADDED ADMIN, OFFICERS & VEHICLES TO DATABASE!')

    offence1 = Offence('Failure to obey traffic signal', 'F100', 5000, 8)
    offence2 = Offence('Exceeding the speed limit', 'E200', 7000, 12)

    
    db.session.add(offence1)
    db.session.add(offence2)
    db.session.add(vehicleOwner1)
    db.session.add(vehicleOwner2)
    db.session.add(vehicleOwner3)
    db.session.add(vehicleOwner4)
    db.session.add(vehicleOwner5)
    db.session.add(vehicleOwner6)
    db.session.add(vehicleOwner7)
    db.session.add(vehicleOwner8)


    db.session.commit()
    print('ADDED OFFENCES, VEHICLE OWNERS TO DB!')

    location1 = Location('27 Constant Spring Road, Kingston 3', 'Kingston')
    location2 = Location('48 Old Hope Road, Kingston 7', 'Kingston')
    location3 = Location('9 Darling Street, Kingston 13', 'Kingston')
    location4 = Location('31B Mona Road, Kingston 5', 'Kingston')
    location5 = Location('3 Molynes Road, Kingston 4', 'Kingston')

    
    db.session.add(location1)
    db.session.add(location2)
    db.session.add(location3)
    db.session.add(location4)
    db.session.add(location5)

    db.session.commit()
    print('ADDED LOCATIONS TO DB!') '''


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


# @app.errorhandler(404)
# def page_not_found(error):
#     """Custom 404 page."""
#     return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")