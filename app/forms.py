from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DecimalField, BooleanField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    isAdmin = BooleanField('Admin Account')

class IssueTicketForm(FlaskForm):
    date = StringField('Date', validators=[InputRequired()])
    time = StringField('Time', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    parish = StringField('Parish', validators=[InputRequired()])
    offence = StringField('Offence', validators=[InputRequired()])
    snapshot = FileField('Snapshot',
        validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], '.jpg, .jpeg and .png Images only!')]
    )

class TrafficTicket(FlaskForm):
    offenceDate = StringField('Date of offence', validators=[DataRequired()])
    offenceTime = StringField('Date of offence', validators=[DataRequired()])
    driverlicencenumber = StringField('Driver Licence Number', validators=[InputRequired()])
    expirationDate = StringField('Expiration Date', validators=[DataRequired()])
    licenseType = StringField('License Type', validators=[DataRequired()])
    licensedIssued = StringField('Country of Issuance', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    firstName = StringField('First Name', validators=[DataRequired()])
    middleName = StringField('Middle Name', validators=[DataRequired()])
    dateofbirth = StringField('Date of Offence', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    address = StringField('Home Address', validators=[DataRequired()])
    streetName = StringField('Street Name', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()]) 
    parish = StringField('Parish', validators=[DataRequired()])
    vehicleType = StringField('Type of Vehicle ', validators=[DataRequired()])
    registrationplatenumber = StringField('Registration Plate Number', validators=[DataRequired()])
    licenseDiscNumber = StringField('License Disc Number', validators=[DataRequired()])
    expirationDate = StringField('Expiration Date', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    colour = StringField('Colour', validators=[DataRequired()])
    offenceLocation = StringField('Location of Offence', validators=[DataRequired()])
    offenceParish = StringField('Parish of Offence', validators=[DataRequired()])
    offenceDescription = StringField('Description of Offence', validators=[DataRequired()])
    toCode = StringField('TO Code', validators=[DataRequired()])
    fine = StringField('Fine', validators=[DataRequired()])
    paymentDeadline = StringField('Payment Deadline', validators=[DataRequired()])
    pointsAssigned = StringField('Points Assigned', validators=[DataRequired()])
    camSnapshot = FileField('Snapshot', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], '.jpg, .jpeg and .png Images only!')])
    trafficTicketNumber = StringField('Points Assigned', validators=[DataRequired()])
    
